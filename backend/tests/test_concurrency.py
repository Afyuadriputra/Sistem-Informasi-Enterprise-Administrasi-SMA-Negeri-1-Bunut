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
def concurrency_env(db):
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

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(attempt_transition, i) for i in range(5)]
        results = [f.result() for f in futures]

    successes = [r for r in results if r == 200]
    conflicts = [r for r in results if r == 409]

    # Exactly 1 thread must succeed, remaining 4 get 409 Conflict
    assert len(successes) == 1, f"Expected 1 success, got {len(successes)}. Results: {results}"
    assert len(conflicts) == 4, f"Expected 4 conflicts, got {len(conflicts)}. Results: {results}"

    # Verify final version in database is 2
    updated_case = StudentCase.objects.get(id=case_id)
    assert updated_case.version == 2
    assert updated_case.status == CaseStatusEnum.DIPROSES


@pytest.mark.django_db(transaction=True)
def test_service_request_optimistic_locking_race_condition(concurrency_env):
    """When multiple threads attempt to transition the same service request with version 1, exactly one succeeds."""
    sr_id = concurrency_env["request"].id
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

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(attempt_transition, i) for i in range(5)]
        results = [f.result() for f in futures]

    successes = [r for r in results if r == 200]
    conflicts = [r for r in results if r == 409]

    assert len(successes) == 1, f"Expected 1 success, got {len(successes)}. Results: {results}"
    assert len(conflicts) == 4, f"Expected 4 conflicts, got {len(conflicts)}. Results: {results}"

    updated_req = ServiceRequest.objects.get(id=sr_id)
    assert updated_req.version == 2
