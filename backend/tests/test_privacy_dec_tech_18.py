import pytest

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Employee,
    Enrollment,
    SchoolClass,
    Student,
)
from apps.student_affairs.models import CaseEvent, CaseStatusEnum, StudentCase


@pytest.fixture
def privacy_env(db):
    roles = {
        name: Role.objects.create(name=name)
        for name in ["Administrator", "Pimpinan", "Kesiswaan", "Tata Usaha", "Wali Kelas", "Guru"]
    }

    users = {}
    tokens = {}
    for role_name in roles:
        u = User.objects.create_user(
            username=f"priv_{role_name.lower().replace(' ', '_')}",
            password="Password123!",
        )
        UserRole.objects.create(user=u, role=roles[role_name])
        users[role_name] = u
        tokens[role_name] = issue_token_pair(u)["access_token"]

    # Academic structure
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-01", end_date="2026-12-31", is_active=True
    )
    cls1 = SchoolClass.objects.create(academic_year=ay, name="X-1", level=10)
    cls2 = SchoolClass.objects.create(academic_year=ay, name="X-2", level=10)

    std = Student.objects.create(student_number="10099", name="Siswa Sensitif", gender="L", status="AKTIF")
    Enrollment.objects.create(student=std, school_class=cls1, start_date="2026-07-01")

    # Wali Kelas 1 (homeroom teacher for X-1)
    emp_wali1 = Employee.objects.create(user=users["Wali Kelas"], nip="198101", name="Wali X-1")
    ClassAssignment.objects.create(employee=emp_wali1, school_class=cls1, role="WALI_KELAS", start_date="2026-07-01")

    # Another teacher (Wali for X-2)
    u_wali2 = User.objects.create_user(username="priv_wali_2", password="Password123!")
    UserRole.objects.create(user=u_wali2, role=roles["Wali Kelas"])
    emp_wali2 = Employee.objects.create(user=u_wali2, nip="198102", name="Wali X-2")
    ClassAssignment.objects.create(employee=emp_wali2, school_class=cls2, role="WALI_KELAS", start_date="2026-07-01")
    tokens["Wali Kelas 2"] = issue_token_pair(u_wali2)["access_token"]

    # Student Case
    sc = StudentCase.objects.create(
        student=std,
        title="Masalah Psikologis & Kedisiplinan",
        summary="Siswa sering murung dan terlambat.",
        status=CaseStatusEnum.DIPROSES,
        version=1,
    )

    # Initial action
    CaseEvent.objects.create(
        case=sc,
        actor=users["Kesiswaan"],
        action="PROSES",
        initial_status=CaseStatusEnum.BARU,
        final_status=CaseStatusEnum.DIPROSES,
        note="Kasus mulai diproses oleh tim bimbingan konseling.",
    )

    # Highly confidential counseling note
    CaseEvent.objects.create(
        case=sc,
        actor=users["Kesiswaan"],
        action="CATAT_TINDAKAN",
        initial_status=CaseStatusEnum.DIPROSES,
        final_status=CaseStatusEnum.DIPROSES,
        note="Sesi konseling mendalam: siswa mengalami trauma masa kecil yang sangat sensitif.",
    )

    return {
        "users": users,
        "tokens": tokens,
        "case": sc,
        "student": std,
    }


@pytest.mark.django_db
def test_dec_tech_18_wali_kelas_masked_counseling_notes(client, privacy_env):
    """Wali Kelas sees case details but CATAT_TINDAKAN notes are strictly masked server-side."""
    case_id = privacy_env["case"].id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {privacy_env['tokens']['Wali Kelas']}"}

    res = client.get(f"/api/student-affairs/cases/{case_id}", **headers)
    assert res.status_code == 200
    data = res.json()

    assert data["id"] == case_id
    assert len(data["events"]) == 2

    # Event 0: PROSES action note is normal
    assert "mulai diproses" in data["events"][0]["note"]

    # Event 1: CATAT_TINDAKAN must be masked!
    counseling_event = data["events"][1]
    assert counseling_event["action"] == "CATAT_TINDAKAN"
    assert counseling_event["note"] == "[Catatan konseling privat - Terproteksi]"
    assert "trauma" not in counseling_event["note"]


@pytest.mark.django_db
def test_dec_tech_18_kesiswaan_sees_unmasked_notes(client, privacy_env):
    """Kesiswaan (counselor) sees complete unmasked counseling notes."""
    case_id = privacy_env["case"].id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {privacy_env['tokens']['Kesiswaan']}"}

    res = client.get(f"/api/student-affairs/cases/{case_id}", **headers)
    assert res.status_code == 200
    data = res.json()

    counseling_event = data["events"][1]
    assert counseling_event["action"] == "CATAT_TINDAKAN"
    assert "trauma masa kecil yang sangat sensitif" in counseling_event["note"]


@pytest.mark.django_db
def test_dec_tech_18_unassigned_wali_denied(client, privacy_env):
    """Wali Kelas of a different class is denied access to student's case."""
    case_id = privacy_env["case"].id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {privacy_env['tokens']['Wali Kelas 2']}"}

    res = client.get(f"/api/student-affairs/cases/{case_id}", **headers)
    assert res.status_code == 403


@pytest.mark.django_db
def test_dec_tech_18_standalone_admin_and_pimpinan_denied_counseling(client, privacy_env):
    """Standalone Administrator and Pimpinan are denied access to sensitive case details."""
    case_id = privacy_env["case"].id

    admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {privacy_env['tokens']['Administrator']}"}
    res_admin = client.get(f"/api/student-affairs/cases/{case_id}", **admin_headers)
    assert res_admin.status_code == 403

    pimpinan_headers = {"HTTP_AUTHORIZATION": f"Bearer {privacy_env['tokens']['Pimpinan']}"}
    res_pimpinan = client.get(f"/api/student-affairs/cases/{case_id}", **pimpinan_headers)
    assert res_pimpinan.status_code == 403


@pytest.mark.django_db
def test_dec_tech_18_catat_tindakan_requires_notes(client, privacy_env):
    """CATAT_TINDAKAN transition requires non-empty notes."""
    case_id = privacy_env["case"].id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {privacy_env['tokens']['Kesiswaan']}"}

    # Attempt with empty notes -> 422
    payload = {
        "action": "CATAT_TINDAKAN",
        "note": "   ",
        "expected_version": 1,
    }
    res = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data=payload,
        content_type="application/json",
        **headers,
    )
    assert res.status_code == 422
    assert "catatan tindakan" in res.json()["message"].lower()
