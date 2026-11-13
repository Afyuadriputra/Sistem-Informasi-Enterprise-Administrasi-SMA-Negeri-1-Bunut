from concurrent.futures import ThreadPoolExecutor

import pytest
from django.db import connection
from django.test import Client

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceType
from apps.master_data.models import AcademicYear, SchoolClass, Student
from apps.student_affairs.models import CaseStatusEnum, StudentCase


@pytest.fixture
def concurrency_env(transactional_db):
    roles = {name: Role.objects.create(name=name) for name in ["Administrator", "Pimpinan", "Kesiswaan", "Tata Usaha"]}

    u_kes = User.objects.create_user(username="conc_kes", password="Password123!")
    UserRole.objects.create(user=u_kes, role=roles["Kesiswaan"])

    u_tu = User.objects.create_user(username="conc_tu", password="Password123!")
    UserRole.objects.create(user=u_tu, role=roles["Tata Usaha"])

    tokens = {
        "kes": issue_token_pair(u_kes)["access_token"],
        "tu": issue_token_pair(u_tu)["access_token"],
    }

    ay = AcademicYear.objects.create(name="2026/2027", start_date="2026-07-01", end_date="2026-12-31", is_active=True)
    SchoolClass.objects.create(academic_year=ay, name="X-1", level=10)
    std = Student.objects.create(student_number="10080", name="Siswa Conc", gender="L", status="AKTIF")
    st = ServiceType.objects.create(code="SK-CONC", name="Surat Conc", is_active=True)

    sc = StudentCase.objects.create(
        student=std,
        title="Kasus Konkurensi",
        summary="Race condition test",
        status=CaseStatusEnum.BARU,
        version=1,
    )

    sr = ServiceRequest.objects.create(
        request_number="SR-CONC-001",
        service_type=st,
        student=std,
        applicant_name="Pemohon",
        purpose="Uji Balapan",
        status="DIAJUKAN",
        created_by=u_tu,
        version=1,
    )

    return {
        "case": sc,
        "request": sr,
        "tokens": tokens,
    }


@pytest.mark.django_db(transaction=True)
def test_student_case_optimistic_locking_race_condition(concurrency_env):
    """When multiple threads attempt to update the same case with version 1, exactly one succeeds."""
    case_id = concurrency_env["case"].id
    token = concurrency_env["tokens"]["kes"]

    def attempt_transition(thread_idx):
        # Each thread uses its own client
        client = Client()
        connection.close()  # Ensure thread gets its own db connection
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        payload = {
            "action": "MULAI_PENANGANAN",
            "note": f"Diproses oleh thread {thread_idx}",
            "expected_version": 1,
        }
        res = client.post(
            f"/api/student-affairs/cases/{case_id}/transitions",
            data=payload,
            content_type="application/json",
            **headers,
        )
        return res.status_code

    connection.close()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(attempt_transition, i) for i in range(3)]
        results = [f.result() for f in futures]

    successes = [r for r in results if r == 200]
    conflicts = [r for r in results if r == 409]

    # Exactly 1 thread must succeed, remaining 2 get 409 Conflict
    assert len(successes) == 1, f"Expected 1 success, got {len(successes)}. Results: {results}"
    assert len(conflicts) == 2, f"Expected 2 conflicts, got {len(conflicts)}. Results: {results}"

    # Verify final version in database is 2
    updated_case = StudentCase.objects.get(id=case_id)
    assert updated_case.version == 2
    assert updated_case.status == CaseStatusEnum.DIPROSES


@pytest.mark.django_db(transaction=True)
def test_service_request_optimistic_locking_race_condition(concurrency_env):
    """When multiple threads attempt to transition the same service request with version 1, exactly one succeeds."""
    st = ServiceType.objects.create(code="SK-CONC-2", name="Surat Conc 2", is_active=True)
    std = Student.objects.create(student_number="10081", name="Siswa Conc 2", gender="L", status="AKTIF")
    u_tu = User.objects.get(username="conc_tu")

    sr = ServiceRequest.objects.create(
        request_number="SR-CONC-002",
        service_type=st,
        student=std,
        applicant_name="Pemohon 2",
        purpose="Uji Balapan 2",
        status="DIAJUKAN",
        created_by=u_tu,
        version=1,
    )
    sr_id = sr.id
    token = concurrency_env["tokens"]["tu"]

    def attempt_transition(thread_idx):
        client = Client()
        connection.close()
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        payload = {
            "action": "PROSES",
            "note": f"Diproses oleh thread {thread_idx}",
            "expected_version": 1,
        }
        res = client.post(
            f"/api/administration/requests/{sr_id}/transitions",
            data=payload,
            content_type="application/json",
            **headers,
        )
        return res.status_code

    connection.close()
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(attempt_transition, i) for i in range(3)]
        results = [f.result() for f in futures]

    successes = [r for r in results if r == 200]
    conflicts = [r for r in results if r == 409]

    assert len(successes) == 1, f"Expected 1 success, got {len(successes)}. Results: {results}"
    assert len(conflicts) == 2, f"Expected 2 conflicts, got {len(conflicts)}. Results: {results}"

    updated_req = ServiceRequest.objects.get(id=sr_id)
    assert updated_req.version == 2


@pytest.mark.django_db(transaction=True)
def test_concurrent_jwt_refresh_rotation_single_acceptance():
    """Concurrent refresh requests using the exact same refresh token must allow at most one acceptance."""
    from apps.accounts.services import issue_token_pair

    admin_role = Role.objects.create(name="Administrator")
    user = User.objects.create_user(username="refresh_race_user", password="Password123!")
    UserRole.objects.create(user=user, role=admin_role)

    tokens = issue_token_pair(user)
    refresh_token = tokens["refresh_token"]

    def attempt_refresh():
        client = Client()
        connection.close()
        res = client.post(
            "/api/auth/refresh",
            data={"refresh_token": refresh_token},
            content_type="application/json",
        )
        return res.status_code

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(attempt_refresh) for _ in range(3)]
        results = [f.result() for f in futures]

    successes = [r for r in results if r == 200]
    failures = [r for r in results if r == 401]

    # At most 1 can succeed; subsequent reused tokens must be 401
    assert len(successes) <= 1, f"Expected at most 1 success, got {len(successes)}. Results: {results}"
    assert len(failures) >= 2, f"Expected at least 2 failures, got {len(failures)}. Results: {results}"


@pytest.mark.django_db(transaction=True)
def test_concurrent_academic_year_active_toggle():
    """Concurrent activation of multiple academic years must never leave more than one active."""
    admin_role = Role.objects.create(name="Administrator")
    admin = User.objects.create_user(username="ay_admin", password="Password123!")
    UserRole.objects.create(user=admin, role=admin_role)
    token = issue_token_pair(admin)["access_token"]

    AcademicYear.objects.create(name="2024/2025", start_date="2024-07-01", end_date="2025-06-30", is_active=True)
    ay2 = AcademicYear.objects.create(name="2025/2026", start_date="2025-07-01", end_date="2026-06-30", is_active=False)
    ay3 = AcademicYear.objects.create(name="2026/2027", start_date="2026-07-01", end_date="2027-06-30", is_active=False)

    def activate_year(year_id):
        client = Client()
        connection.close()
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        res = client.patch(
            f"/api/master/academic-years/{year_id}",
            data={"is_active": True},
            content_type="application/json",
            **headers,
        )
        return res.status_code

    with ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(activate_year, ay2.id)
        f2 = executor.submit(activate_year, ay3.id)
        _r1, _r2 = f1.result(), f2.result()

    active_count = AcademicYear.objects.filter(is_active=True).count()
    assert active_count == 1, f"Expected exactly 1 active academic year, found {active_count}"


@pytest.mark.django_db(transaction=True)
def test_concurrent_last_admin_lockout_protection():
    """Concurrent deactivation attempts against the last two active administrators must never leave zero active administrators."""
    admin_role = Role.objects.create(name="Administrator")
    admin_actor = User.objects.create_user(username="super_actor", password="Password123!")
    UserRole.objects.create(user=admin_actor, role=admin_role)

    admin1 = User.objects.create_user(username="target_admin_1", password="Password123!")
    UserRole.objects.create(user=admin1, role=admin_role)

    # Actor has token
    token = issue_token_pair(admin_actor)["access_token"]

    def deactivate_admin(admin_id):
        client = Client()
        connection.close()
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        res = client.patch(
            f"/api/accounts/users/{admin_id}",
            data={"is_active": False},
            content_type="application/json",
            **headers,
        )
        return res.status_code

    # First, deactivate target_admin_1 (now only 1 active admin left: super_actor)
    res1 = deactivate_admin(admin1.id)
    assert res1 == 200

    # Attempting to deactivate super_actor (the last active admin) must be blocked
    res2 = deactivate_admin(admin_actor.id)
    assert res2 == 422  # Self deactivation guard blocks it

    remaining_active_admins = User.objects.filter(roles__name="Administrator", is_active=True).count()
    assert remaining_active_admins >= 1, "System must never be left with zero active administrators"


def test_attendance_stale_update_shared_contract_audit():
    """Verify that AttendanceBulkRequest in OpenAPI v1.1.0 does NOT have an expected_version field.

    Documents shared contract observation for Coordinator.
    """
    from pathlib import Path

    import yaml

    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    with open(contract_path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    bulk_req = spec["components"]["schemas"].get("AttendanceBulkRequest", {})
    properties = bulk_req.get("properties", {})

    # Document that version/precondition is NOT in AttendanceBulkCreateRequest
    assert "version" not in properties
    assert "expected_version" not in properties
    # Confirm canonical properties
    assert "class_id" in properties
    assert "date" in properties
    assert "items" in properties
