import pytest
from django.test import Client

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


@pytest.fixture
def case_setup(db):
    kesiswaan_role = Role.objects.create(name="Kesiswaan")
    wali_role = Role.objects.create(name="Wali Kelas")

    # Kesiswaan user
    user_kes = User.objects.create_user(username="kesiswaan1", password="Password123!")
    UserRole.objects.create(user=user_kes, role=kesiswaan_role)
    emp_kes = Employee.objects.create(user=user_kes, nip="198201", name="Staf Kesiswaan")

    # Wali Kelas user for Class A
    user_wali = User.objects.create_user(username="wali_a", password="Password123!")
    UserRole.objects.create(user=user_wali, role=wali_role)
    emp_wali = Employee.objects.create(user=user_wali, nip="198202", name="Wali Kelas A")

    # Wali Kelas user for Class B
    user_wali_b = User.objects.create_user(username="wali_b", password="Password123!")
    UserRole.objects.create(user=user_wali_b, role=wali_role)
    emp_wali_b = Employee.objects.create(user=user_wali_b, nip="198203", name="Wali Kelas B")

    # Classes
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-01", end_date="2026-12-31", is_active=True
    )
    cls_a = SchoolClass.objects.create(academic_year=ay, name="X-A", level=10)
    cls_b = SchoolClass.objects.create(academic_year=ay, name="X-B", level=10)

    # Assignments
    ClassAssignment.objects.create(
        employee=emp_wali, school_class=cls_a, role="WALI_KELAS", start_date="2026-07-01"
    )
    ClassAssignment.objects.create(
        employee=emp_wali_b, school_class=cls_b, role="WALI_KELAS", start_date="2026-07-01"
    )

    # Students
    std_a = Student.objects.create(student_number="S101", name="Siswa A", gender="LAKI_LAKI")
    Enrollment.objects.create(student=std_a, school_class=cls_a, start_date="2026-07-01")

    std_b = Student.objects.create(student_number="S102", name="Siswa B", gender="PEREMPUAN")
    Enrollment.objects.create(student=std_b, school_class=cls_b, start_date="2026-07-01")

    return {
        "kesiswaan_token": issue_token_pair(user_kes)["access_token"],
        "wali_token": issue_token_pair(user_wali)["access_token"],
        "wali_b_token": issue_token_pair(user_wali_b)["access_token"],
        "std_a": std_a,
        "std_b": std_b,
        "emp_kes": emp_kes,
    }


@pytest.mark.django_db
def test_optimistic_concurrency_conflict_be_06(client: Client, case_setup):
    """BE-06: Stale update on student case returns HTTP 409 Conflict."""
    setup = case_setup
    headers = {"HTTP_AUTHORIZATION": f"Bearer {setup['kesiswaan_token']}"}

    # 1. Create case (version=1, status=BARU)
    create_res = client.post(
        "/api/student-affairs/cases",
        data={
            "student_id": setup["std_a"].id,
            "title": "Kasus Pelanggaran Tata Tertib",
            "summary": "Siswa sering terlambat ke sekolah.",
            "assigned_to_id": setup["emp_kes"].id,
        },
        content_type="application/json",
        **headers,
    )
    assert create_res.status_code == 201
    case_id = create_res.json()["id"]
    assert create_res.json()["version"] == 1

    # 2. First actor transitions with expected_version=1 -> succeeds (version becomes 2)
    t1_res = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={
            "action": "MULAI_PENANGANAN",
            "note": "Memulai konseling pertama dengan siswa.",
            "expected_version": 1,
        },
        content_type="application/json",
        **headers,
    )
    assert t1_res.status_code == 200
    assert t1_res.json()["version"] == 2
    assert t1_res.json()["status"] == "DIPROSES"

    # 3. Second actor attempts transition with stale expected_version=1 -> HTTP 409 Conflict
    t2_res = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={
            "action": "CATAT_TINDAKAN",
            "note": "Mencatat panggilan orang tua.",
            "expected_version": 1,
        },
        content_type="application/json",
        **headers,
    )
    assert t2_res.status_code == 409
    data = t2_res.json()
    assert data["code"] == "CONCURRENCY_CONFLICT"
    assert "telah diubah oleh pengguna lain" in data["message"]


@pytest.mark.django_db
def test_state_machine_transitions_and_terminal_status(client: Client, case_setup):
    """Test state machine flow: BARU -> DIPROSES -> SELESAI and rejection on terminal state."""
    setup = case_setup
    headers = {"HTTP_AUTHORIZATION": f"Bearer {setup['kesiswaan_token']}"}

    create_res = client.post(
        "/api/student-affairs/cases",
        data={
            "student_id": setup["std_a"].id,
            "title": "Bimbingan Belajar",
            "summary": "Nilai akademik menurun.",
        },
        content_type="application/json",
        **headers,
    )
    case_id = create_res.json()["id"]

    # Invalid jump directly from BARU to SELESAIKAN -> 422
    bad_jump = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "SELESAIKAN", "note": "Langsung selesai", "expected_version": 1},
        content_type="application/json",
        **headers,
    )
    assert bad_jump.status_code == 422

    # Transition to DIPROSES
    client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "MULAI_PENANGANAN", "note": "Konseling dimulai", "expected_version": 1},
        content_type="application/json",
        **headers,
    )

    # Record intermediate action
    client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "CATAT_TINDAKAN", "note": "Pertemuan dengan guru mapel", "expected_version": 2},
        content_type="application/json",
        **headers,
    )

    # Transition to SELESAI
    selesai_res = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "SELESAIKAN", "note": "Nilai membaik dan masalah tuntas", "expected_version": 3},
        content_type="application/json",
        **headers,
    )
    assert selesai_res.status_code == 200
    assert selesai_res.json()["status"] == "SELESAI"

    # Attempt transition on terminal state SELESAI -> 422
    term_res = client.post(
        f"/api/student-affairs/cases/{case_id}/transitions",
        data={"action": "CATAT_TINDAKAN", "note": "Catatan tambahan", "expected_version": 4},
        content_type="application/json",
        **headers,
    )
    assert term_res.status_code == 422
    assert "status akhir" in term_res.json()["message"]


@pytest.mark.django_db
def test_wali_kelas_object_level_privacy(client: Client, case_setup):
    """Test Wali Kelas can only view cases of students in their assigned class."""
    setup = case_setup
    kes_headers = {"HTTP_AUTHORIZATION": f"Bearer {setup['kesiswaan_token']}"}
    wali_a_headers = {"HTTP_AUTHORIZATION": f"Bearer {setup['wali_token']}"}
    wali_b_headers = {"HTTP_AUTHORIZATION": f"Bearer {setup['wali_b_token']}"}

    # Create case for student in Class A
    case_res = client.post(
        "/api/student-affairs/cases",
        data={
            "student_id": setup["std_a"].id,
            "title": "Konseling Pribadi Siswa A",
            "summary": "Catatan konseling privat kelas A.",
        },
        content_type="application/json",
        **kes_headers,
    )
    case_id = case_res.json()["id"]

    # Wali Kelas A can view detail
    ok_res = client.get(f"/api/student-affairs/cases/{case_id}", **wali_a_headers)
    assert ok_res.status_code == 200
    assert len(ok_res.json()["events"]) >= 1

    # Wali Kelas B cannot view detail of student in Class A -> 403 Forbidden
    forbidden_res = client.get(f"/api/student-affairs/cases/{case_id}", **wali_b_headers)
    assert forbidden_res.status_code == 403
    assert "tidak memiliki wewenang" in forbidden_res.json()["message"]
