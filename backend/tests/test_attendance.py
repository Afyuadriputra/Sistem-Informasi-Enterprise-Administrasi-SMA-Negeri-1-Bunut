from datetime import date, timedelta

import pytest
from django.test import Client

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.attendance.models import Attendance
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Employee,
    Enrollment,
    SchoolClass,
    Student,
)


@pytest.fixture
def attendance_setup(db):
    guru_role = Role.objects.create(name="Guru")
    admin_role = Role.objects.create(name="Administrator")

    # Teachers
    user_guru1 = User.objects.create_user(username="guru1", password="Password123!")
    UserRole.objects.create(user=user_guru1, role=guru_role)
    emp1 = Employee.objects.create(user=user_guru1, nip="198101", name="Guru Satu")

    user_guru2 = User.objects.create_user(username="guru2", password="Password123!")
    UserRole.objects.create(user=user_guru2, role=guru_role)
    Employee.objects.create(user=user_guru2, nip="198102", name="Guru Dua")

    admin = User.objects.create_user(username="admin_att", password="Password123!")
    UserRole.objects.create(user=admin, role=admin_role)

    # Class & Academic Year
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-01", end_date="2026-12-31", is_active=True
    )
    cls1 = SchoolClass.objects.create(academic_year=ay, name="X-A", level=10)
    cls2 = SchoolClass.objects.create(academic_year=ay, name="X-B", level=10)

    # Assign Guru 1 to Class 1 only
    ClassAssignment.objects.create(employee=emp1, school_class=cls1, role="GURU_MAPEL", start_date="2026-07-01")

    # Students enrolled in Class 1
    std1 = Student.objects.create(student_number="S001", name="Siswa Satu", gender="LAKI_LAKI")
    std2 = Student.objects.create(student_number="S002", name="Siswa Dua", gender="PEREMPUAN")
    Enrollment.objects.create(student=std1, school_class=cls1, start_date="2026-07-01")
    Enrollment.objects.create(student=std2, school_class=cls1, start_date="2026-07-01")

    # Student enrolled in Class 2
    std3 = Student.objects.create(student_number="S003", name="Siswa Tiga", gender="LAKI_LAKI")
    Enrollment.objects.create(student=std3, school_class=cls2, start_date="2026-07-01")

    return {
        "guru1_token": issue_token_pair(user_guru1)["access_token"],
        "guru2_token": issue_token_pair(user_guru2)["access_token"],
        "admin_token": issue_token_pair(admin)["access_token"],
        "class1": cls1,
        "class2": cls2,
        "std1": std1,
        "std2": std2,
        "std3": std3,
    }


@pytest.mark.django_db
def test_teacher_outside_assignment_rejected_be_03(client: Client, attendance_setup):
    """BE-03: Guru A trying to record attendance for a class not assigned returns 403."""
    setup = attendance_setup
    today_str = date.today().isoformat()

    # Guru 2 tries to record attendance for Class 1 (assigned to Guru 1)
    res = client.post(
        "/api/attendance/bulk",
        data={
            "class_id": setup["class1"].id,
            "date": today_str,
            "items": [{"student_id": setup["std1"].id, "status": "HADIR", "note": ""}],
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {setup['guru2_token']}",
    )
    assert res.status_code == 403
    assert Attendance.objects.count() == 0


@pytest.mark.django_db
def test_unenrolled_student_causes_atomic_rollback_be_04(client: Client, attendance_setup):
    """BE-04: Batch containing student from another class is rejected (422) with 0 rows saved."""
    setup = attendance_setup
    today_str = date.today().isoformat()

    # Payload has valid std1 (in class 1) and invalid std3 (in class 2)
    res = client.post(
        "/api/attendance/bulk",
        data={
            "class_id": setup["class1"].id,
            "date": today_str,
            "items": [
                {"student_id": setup["std1"].id, "status": "HADIR", "note": ""},
                {"student_id": setup["std3"].id, "status": "HADIR", "note": ""},
            ],
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {setup['guru1_token']}",
    )
    assert res.status_code == 422
    assert "tidak terdaftar" in res.json()["message"]
    # Verify complete atomic rollback
    assert Attendance.objects.count() == 0


@pytest.mark.django_db
def test_valid_bulk_attendance_and_history_snapshot_be_05(client: Client, attendance_setup):
    """BE-05: Valid bulk attendance saves all rows, creates historical snapshot, and recap updates."""
    setup = attendance_setup
    today_str = date.today().isoformat()

    res = client.post(
        "/api/attendance/bulk",
        data={
            "class_id": setup["class1"].id,
            "date": today_str,
            "items": [
                {"student_id": setup["std1"].id, "status": "HADIR", "note": ""},
                {"student_id": setup["std2"].id, "status": "SAKIT", "note": "Demam"},
            ],
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {setup['guru1_token']}",
    )
    assert res.status_code == 200
    assert res.json()["saved_count"] == 2

    # Verify database persistence
    assert Attendance.objects.filter(school_class=setup["class1"]).count() == 2

    # Verify bulk history snapshots created via simple-history
    assert Attendance.history.count() == 2

    # Verify roster reflects saved status
    roster_res = client.get(
        f"/api/attendance/roster?class_id={setup['class1'].id}&date={today_str}",
        HTTP_AUTHORIZATION=f"Bearer {setup['guru1_token']}",
    )
    assert roster_res.status_code == 200
    roster_data = roster_res.json()
    assert len(roster_data["students"]) == 2
    statuses = {s["student_id"]: s["current_status"] for s in roster_data["students"]}
    assert statuses[setup["std1"].id] == "HADIR"
    assert statuses[setup["std2"].id] == "SAKIT"

    # Verify recap calculation
    recap_res = client.get(
        f"/api/attendance?class_id={setup['class1'].id}",
        HTTP_AUTHORIZATION=f"Bearer {setup['guru1_token']}",
    )
    assert recap_res.status_code == 200
    recap_data = recap_res.json()
    assert recap_data["summary"]["total_students"] == 2
    assert recap_data["summary"]["sakit_count"] == 1
    assert recap_data["summary"]["hadir_pct"] == 50.0


@pytest.mark.django_db
def test_future_date_attendance_rejected(client: Client, attendance_setup):
    """Test attendance date in the future is rejected with 422."""
    setup = attendance_setup
    future_date = (date.today() + timedelta(days=2)).isoformat()

    res = client.post(
        "/api/attendance/bulk",
        data={
            "class_id": setup["class1"].id,
            "date": future_date,
            "items": [{"student_id": setup["std1"].id, "status": "HADIR", "note": ""}],
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {setup['guru1_token']}",
    )
    assert res.status_code == 422
    assert "tidak boleh melebihi tanggal berjalan" in res.json()["message"]
