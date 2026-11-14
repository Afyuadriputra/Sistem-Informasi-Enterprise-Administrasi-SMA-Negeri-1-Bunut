from datetime import date
from concurrent.futures import ThreadPoolExecutor
import pytest
from django.db import connection
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
def attendance_concurrency_env(transactional_db):
    role_guru = Role.objects.create(name="Guru")

    # Teacher 1
    u1 = User.objects.create_user(username="guru_conc_1", password="Password123!")
    UserRole.objects.create(user=u1, role=role_guru)
    emp1 = Employee.objects.create(user=u1, nip="197001", name="Guru Conc 1")

    # Teacher 2
    u2 = User.objects.create_user(username="guru_conc_2", password="Password123!")
    UserRole.objects.create(user=u2, role=role_guru)
    emp2 = Employee.objects.create(user=u2, nip="197002", name="Guru Conc 2")

    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 12, 31),
        is_active=True,
    )
    cls = SchoolClass.objects.create(academic_year=ay, name="X-CONC", level=10)

    # Assign both teachers to class X-CONC
    ClassAssignment.objects.create(
        employee=emp1,
        school_class=cls,
        role="GURU_MAPEL",
        start_date=date(2026, 7, 1),
    )
    ClassAssignment.objects.create(
        employee=emp2,
        school_class=cls,
        role="GURU_MAPEL",
        start_date=date(2026, 7, 1),
    )

    # Enrolled students
    s1 = Student.objects.create(student_number="CONC01", name="Siswa Conc 1", gender="LAKI_LAKI", status="AKTIF")
    s2 = Student.objects.create(student_number="CONC02", name="Siswa Conc 2", gender="PEREMPUAN", status="AKTIF")
    Enrollment.objects.create(student=s1, school_class=cls, start_date=date(2026, 7, 1))
    Enrollment.objects.create(student=s2, school_class=cls, start_date=date(2026, 7, 1))

    return {
        "class": cls,
        "teacher1_token": issue_token_pair(u1)["access_token"],
        "teacher2_token": issue_token_pair(u2)["access_token"],
        "students": [s1, s2],
    }


@pytest.mark.django_db(transaction=True)
def test_attendance_stale_roster_rejection_409(attendance_concurrency_env):
    """Verify that submitting bulk attendance with a stale roster revision returns HTTP 409 Conflict (CCR-20261114-01)."""
    env = attendance_concurrency_env
    cls_id = env["class"].id
    today_str = date.today().isoformat()

    client1 = Client()
    headers1 = {"HTTP_AUTHORIZATION": f"Bearer {env['teacher1_token']}"}

    client2 = Client()
    headers2 = {"HTTP_AUTHORIZATION": f"Bearer {env['teacher2_token']}"}

    # 1. Teacher 1 loads roster
    roster_res1 = client1.get(f"/api/attendance/roster?class_id={cls_id}&date={today_str}", **headers1)
    assert roster_res1.status_code == 200
    v1 = roster_res1.json().get("roster_version", 0)

    # 2. Teacher 2 loads roster at same initial revision
    roster_res2 = client2.get(f"/api/attendance/roster?class_id={cls_id}&date={today_str}", **headers2)
    assert roster_res2.status_code == 200
    v2 = roster_res2.json().get("roster_version", 0)
    assert v1 == v2 == 0

    # 3. Teacher 1 saves attendance first with expected_roster_version=0 -> 200 OK
    payload1 = {
        "class_id": cls_id,
        "date": today_str,
        "expected_roster_version": v1,
        "items": [
            {"student_id": env["students"][0].id, "status": "HADIR", "note": "Hadir tepat waktu"},
            {"student_id": env["students"][1].id, "status": "HADIR", "note": ""},
        ],
    }
    save_res1 = client1.post("/api/attendance/bulk", data=payload1, content_type="application/json", **headers1)
    assert save_res1.status_code == 200
    assert save_res1.json()["saved_count"] == 2

    # 4. Teacher 2 attempts to save with stale expected_roster_version=0 -> 409 Conflict!
    payload2 = {
        "class_id": cls_id,
        "date": today_str,
        "expected_roster_version": v2,
        "items": [
            {"student_id": env["students"][0].id, "status": "ALPA", "note": "Stale overwrite attempt"},
            {"student_id": env["students"][1].id, "status": "HADIR", "note": ""},
        ],
    }
    save_res2 = client2.post("/api/attendance/bulk", data=payload2, content_type="application/json", **headers2)
    assert save_res2.status_code == 409
    err_body = save_res2.json()
    assert err_body["code"] == "CONCURRENCY_CONFLICT"
    assert "telah diperbarui oleh pengguna lain" in err_body["message"]

    # 5. Verify Teacher 1's data was NOT overwritten
    from apps.attendance.models import Attendance
    rec1 = Attendance.objects.get(school_class_id=cls_id, student=env["students"][0], date=date.today())
    assert rec1.status == "HADIR"
    assert rec1.note == "Hadir tepat waktu"


@pytest.mark.django_db(transaction=True)
def test_concurrent_attendance_bulk_submissions(attendance_concurrency_env):
    """When two concurrent threads submit bulk attendance with expected_roster_version=0 on a fresh date,
    exactly one succeeds with 200 and the other is rejected with 409 Conflict.
    """
    env = attendance_concurrency_env
    cls_id = env["class"].id
    test_date_str = date(2026, 9, 20).isoformat()
    t1 = env["teacher1_token"]
    t2 = env["teacher2_token"]
    s_ids = [s.id for s in env["students"]]

    def submit_attendance(token, status_val):
        c = Client()
        connection.close()
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        payload = {
            "class_id": cls_id,
            "date": test_date_str,
            "expected_roster_version": 0,
            "items": [
                {"student_id": s_ids[0], "status": status_val, "note": f"Dari {status_val}"},
                {"student_id": s_ids[1], "status": "HADIR", "note": ""},
            ],
        }
        res = c.post("/api/attendance/bulk", data=payload, content_type="application/json", **headers)
        if res.status_code != 200:
            print(f"DEBUG: thread for {status_val} got {res.status_code}: {res.json()}")
        return res.status_code

    connection.close()
    with ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(submit_attendance, t1, "HADIR")
        f2 = executor.submit(submit_attendance, t2, "SAKIT")
        results = [f1.result(), f2.result()]

    successes = [r for r in results if r == 200]
    conflicts = [r for r in results if r == 409]

    assert len(successes) == 1, f"Expected 1 success, got {len(successes)}. Results: {results}"
    assert len(conflicts) == 1, f"Expected 1 conflict, got {len(conflicts)}. Results: {results}"
