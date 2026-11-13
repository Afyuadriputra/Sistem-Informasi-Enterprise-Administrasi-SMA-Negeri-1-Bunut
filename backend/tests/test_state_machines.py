import pytest

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceRequestStatusEnum, ServiceType
from apps.master_data.models import AcademicYear, SchoolClass, Student
from apps.student_affairs.models import CaseStatusEnum, StudentCase


@pytest.fixture
def sm_env(db):
    roles = {name: Role.objects.create(name=name) for name in ["Administrator", "Pimpinan", "Kesiswaan", "Tata Usaha"]}

    users = {}
    tokens = {}
    for role_name in roles:
        u = User.objects.create_user(username=f"sm_{role_name.lower()}", password="Password123!")
        UserRole.objects.create(user=u, role=roles[role_name])
        users[role_name] = u
        tokens[role_name] = issue_token_pair(u)["access_token"]

    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-01", end_date="2026-12-31", is_active=True
    )
    SchoolClass.objects.create(academic_year=ay, name="X-1", level=10)
    std = Student.objects.create(student_number="10050", name="Siswa SM", gender="L", status="AKTIF")

    st_appr = ServiceType.objects.create(
        code="SK-APPR", name="Surat Butuh Approval", requires_approval=True, is_active=True
    )
    st_noappr = ServiceType.objects.create(
        code="SK-DIRECT", name="Surat Langsung", requires_approval=False, is_active=True
    )

    return {
        "users": users,
        "tokens": tokens,
        "student": std,
        "st_appr": st_appr,
        "st_noappr": st_noappr,
    }


@pytest.mark.django_db
def test_student_case_lifecycle_and_terminal_states(client, sm_env):
    """Test full valid lifecycle of student case and assert terminal states."""
    h_kesiswaan = {"HTTP_AUTHORIZATION": f"Bearer {sm_env['tokens']['Kesiswaan']}"}

    # 1. Create case -> BARU (version 1)
    res_c = client.post(
        "/api/student-affairs/cases",
        data={"student_id": sm_env["student"].id, "title": "Kasus Uji SM", "summary": "Ringkasan kasus"},
        content_type="application/json",
        **h_kesiswaan,
    )
    assert res_c.status_code == 201
    case_data = res_c.json()
    case_id = case_data["id"]
    assert case_data["status"] == "BARU"
    assert case_data["version"] == 1

    # 2. Transition BARU -> DIPROSES (action: MULAI_PENANGANAN, version 1 -> 2)
    res_p = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "MULAI_PENANGANAN", "note": "Mulai diproses", "expected_version": 1},
        content_type="application/json",
        **h_kesiswaan,
    )
    assert res_p.status_code == 200
    assert res_p.json()["status"] == "DIPROSES"
    assert res_p.json()["version"] == 2

    # 3. Action: CATAT_TINDAKAN (remains DIPROSES, version 2 -> 3)
    res_act = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "CATAT_TINDAKAN", "note": "Bimbingan dilakukan", "expected_version": 2},
        content_type="application/json",
        **h_kesiswaan,
    )
    assert res_act.status_code == 200
    assert res_act.json()["status"] == "DIPROSES"
    assert res_act.json()["version"] == 3

    # 4. Transition DIPROSES -> SELESAI (action: SELESAIKAN, version 3 -> 4)
    res_fin = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "SELESAIKAN", "note": "Kasus selesai", "expected_version": 3},
        content_type="application/json",
        **h_kesiswaan,
    )
    assert res_fin.status_code == 200
    assert res_fin.json()["status"] == "SELESAI"
    assert res_fin.json()["version"] == 4

    # 5. Terminal state check: SELESAI cannot transition further
    res_term = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "MULAI_PENANGANAN", "note": "Coba buka lagi", "expected_version": 4},
        content_type="application/json",
        **h_kesiswaan,
    )
    assert res_term.status_code == 422
    assert "status akhir" in res_term.json()["message"].lower()


@pytest.mark.django_db
def test_student_case_optimistic_locking(client, sm_env):
    """Mismatched expected_version returns 409 Conflict."""
    h_kesiswaan = {"HTTP_AUTHORIZATION": f"Bearer {sm_env['tokens']['Kesiswaan']}"}

    sc = StudentCase.objects.create(
        student=sm_env["student"],
        title="Kasus Concurrency",
        summary="Test version mismatch",
        status=CaseStatusEnum.BARU,
        version=5,
    )

    # Transition with outdated expected_version 4 -> 409 Conflict
    res_conflict = client.post(
        f"/api/student-affairs/cases/{sc.id}/transitions",
        data={"action": "MULAI_PENANGANAN", "note": "Coba proses", "expected_version": 4},
        content_type="application/json",
        **h_kesiswaan,
    )
    assert res_conflict.status_code == 409
    assert "telah diubah oleh pengguna lain" in res_conflict.json()["message"].lower()


@pytest.mark.django_db
def test_service_request_full_approval_lifecycle(client, sm_env):
    """Test ServiceRequest lifecycle requiring Pimpinan approval."""
    h_tu = {"HTTP_AUTHORIZATION": f"Bearer {sm_env['tokens']['Tata Usaha']}"}
    h_pimpinan = {"HTTP_AUTHORIZATION": f"Bearer {sm_env['tokens']['Pimpinan']}"}

    # 1. Create request -> DIAJUKAN (version 1)
    res_c = client.post(
        "/api/administration/requests",
        data={
            "service_type_id": sm_env["st_appr"].id,
            "student_id": sm_env["student"].id,
            "applicant_name": "Wali Siswa",
            "purpose": "Keperluan dinas",
        },
        content_type="application/json",
        **h_tu,
    )
    assert res_c.status_code == 201
    sr_data = res_c.json()
    sr_id = sr_data["id"]
    assert sr_data["status"] == "DIAJUKAN"
    assert sr_data["version"] == 1

    # 2. TU processes request: DIAJUKAN -> DIPROSES (action: PROSES, version 1 -> 2)
    res_proc = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data={"action": "PROSES", "note": "Mulai diproses berkas", "expected_version": 1},
        content_type="application/json",
        **h_tu,
    )
    assert res_proc.status_code == 200
    assert res_proc.json()["status"] == "DIPROSES"
    assert res_proc.json()["version"] == 2

    # 3. TU submits for approval: DIPROSES -> MENUNGGU_PERSETUJUAN (action: AJUKAN_PERSETUJUAN, version 2 -> 3)
    res_sub = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data={"action": "AJUKAN_PERSETUJUAN", "note": "Mohon tanda tangan", "expected_version": 2},
        content_type="application/json",
        **h_tu,
    )
    assert res_sub.status_code == 200
    assert res_sub.json()["status"] == "MENUNGGU_PERSETUJUAN"
    assert res_sub.json()["version"] == 3

    # 4. Pimpinan approves: MENUNGGU_PERSETUJUAN -> DISETUJUI (action: SETUJUI, version 3 -> 4)
    res_appr = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data={"action": "SETUJUI", "note": "Disetujui kepala sekolah", "expected_version": 3},
        content_type="application/json",
        **h_pimpinan,
    )
    assert res_appr.status_code == 200
    assert res_appr.json()["status"] == "DISETUJUI"
    assert res_appr.json()["version"] == 4

    # 5. TU marks finished: DISETUJUI -> SELESAI (action: SELESAIKAN, version 4 -> 5)
    res_fin = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data={"action": "SELESAIKAN", "note": "Dokumen fisik telah diambil", "expected_version": 4},
        content_type="application/json",
        **h_tu,
    )
    assert res_fin.status_code == 200
    assert res_fin.json()["status"] == "SELESAI"
    assert res_fin.json()["version"] == 5

    # 6. Terminal state check: SELESAI cannot transition further
    res_term = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data={"action": "PROSES", "note": "Coba ulangi", "expected_version": 5},
        content_type="application/json",
        **h_tu,
    )
    assert res_term.status_code == 422


@pytest.mark.django_db
def test_service_request_rejection_terminal_state(client, sm_env):
    """Pimpinan rejects request -> DITOLAK (terminal state)."""
    h_pimpinan = {"HTTP_AUTHORIZATION": f"Bearer {sm_env['tokens']['Pimpinan']}"}

    sr = ServiceRequest.objects.create(
        request_number="SR-REJ-001",
        service_type=sm_env["st_appr"],
        student=sm_env["student"],
        applicant_name="Pemohon",
        purpose="Tujuan",
        status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
        created_by=sm_env["users"]["Tata Usaha"],
        version=2,
    )

    # Rejection requires reason
    res_rej = client.post(
        f"/api/administration/requests/{sr.id}/transitions",
        data={"action": "TOLAK", "note": "Persyaratan berkas kurang lengkap", "expected_version": 2},
        content_type="application/json",
        **h_pimpinan,
    )
    assert res_rej.status_code == 200
    assert res_rej.json()["status"] == "DITOLAK"
    assert res_rej.json()["version"] == 3

    # Attempt transition from DITOLAK -> 422
    res_after = client.post(
        f"/api/administration/requests/{sr.id}/transitions",
        data={"action": "SETUJUI", "note": "Coba setujui setelah tolak", "expected_version": 3},
        content_type="application/json",
        **h_pimpinan,
    )
    assert res_after.status_code == 422
