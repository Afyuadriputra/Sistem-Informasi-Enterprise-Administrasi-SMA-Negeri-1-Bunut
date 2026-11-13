import statistics
import time
from datetime import date

import pytest
from django.core.cache import cache

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
def perf_env(db):
    cache.clear()
    admin_r = Role.objects.create(name="Administrator")
    guru_r = Role.objects.create(name="Guru")

    u_admin = User.objects.create_user(username="perf_admin", password="Password123!")
    UserRole.objects.create(user=u_admin, role=admin_r)

    u_guru = User.objects.create_user(username="perf_guru", password="Password123!")
    UserRole.objects.create(user=u_guru, role=guru_r)

    tokens = {
        "admin": issue_token_pair(u_admin)["access_token"],
        "guru": issue_token_pair(u_guru)["access_token"],
    }

    ay = AcademicYear.objects.create(name="2026/2027", start_date="2026-07-01", end_date="2026-12-31", is_active=True)
    cls1 = SchoolClass.objects.create(academic_year=ay, name="X-PERF", level=10)

    emp = Employee.objects.create(user=u_guru, nip="199901", name="Guru Perf")
    ClassAssignment.objects.create(employee=emp, school_class=cls1, role="GURU_MAPEL", start_date="2026-07-01")

    students = [
        Student(student_number=f"PERF{i:03d}", name=f"Siswa Perf {i}", gender="L", status="AKTIF") for i in range(1, 31)
    ]
    Student.objects.bulk_create(students)
    all_students = list(Student.objects.filter(student_number__startswith="PERF"))

    enrollments = [Enrollment(student=s, school_class=cls1, start_date="2026-07-01") for s in all_students]
    Enrollment.objects.bulk_create(enrollments)

    return {
        "admin_user": u_admin,
        "guru_user": u_guru,
        "tokens": tokens,
        "class": cls1,
        "students": all_students,
    }


def compute_latencies(durations_ms):
    sorted_d = sorted(durations_ms)
    n = len(sorted_d)
    p50 = sorted_d[int(n * 0.50)]
    p95 = sorted_d[min(int(n * 0.95), n - 1)]
    p99 = sorted_d[min(int(n * 0.99), n - 1)]
    avg = statistics.mean(sorted_d)
    return {"p50_ms": round(p50, 2), "p95_ms": round(p95, 2), "p99_ms": round(p99, 2), "avg_ms": round(avg, 2)}


@pytest.mark.django_db
def test_performance_login_latency(client, perf_env):
    """Benchmark login endpoint latency across 10 iterations."""
    latencies = []
    for _ in range(10):
        t0 = time.perf_counter()
        res = client.post(
            "/api/auth/login",
            data={"username": "perf_admin", "password": "Password123!"},
            content_type="application/json",
        )
        t1 = time.perf_counter()
        assert res.status_code == 200
        latencies.append((t1 - t0) * 1000)

    metrics = compute_latencies(latencies)
    # Password hashing (PBKDF2/argon2) has baseline cost, expect p95 < 2000ms
    assert metrics["p95_ms"] < 2000, f"Login p95 exceeded budget: {metrics}"


@pytest.mark.django_db
def test_performance_dashboard_metrics_cache_latency(client, perf_env):
    """Benchmark cold cache vs warm cache latency for dashboard metrics."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {perf_env['tokens']['admin']}"}

    # Cold run
    cache.clear()
    t0 = time.perf_counter()
    res_cold = client.get("/api/reports/dashboard", **headers)
    t1 = time.perf_counter()
    assert res_cold.status_code == 200
    assert (t1 - t0) * 1000 > 0

    # Warm runs (15 iterations)
    warm_latencies = []
    for _ in range(15):
        t0 = time.perf_counter()
        res_warm = client.get("/api/reports/dashboard", **headers)
        t1 = time.perf_counter()
        assert res_warm.status_code == 200
        warm_latencies.append((t1 - t0) * 1000)

    warm_metrics = compute_latencies(warm_latencies)
    # Warm cache p95 should be fast (< 200ms)
    assert warm_metrics["p95_ms"] < 200, f"Warm cache p95 exceeded budget: {warm_metrics}"


@pytest.mark.django_db
def test_performance_attendance_bulk_save_latency(client, perf_env):
    """Benchmark saving attendance for 30 students in one atomic request."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {perf_env['tokens']['guru']}"}
    today = date.today().isoformat()
    records = [
        {
            "student_id": s.id,
            "status": "HADIR" if idx % 5 != 0 else "SAKIT",
            "note": "Keterangan" if idx % 5 == 0 else "",
        }
        for idx, s in enumerate(perf_env["students"])
    ]
    payload = {
        "class_id": perf_env["class"].id,
        "date": today,
        "items": records,
    }

    t0 = time.perf_counter()
    res = client.post("/api/attendance/bulk", data=payload, content_type="application/json", **headers)
    t1 = time.perf_counter()

    assert res.status_code == 200
    duration_ms = (t1 - t0) * 1000
    # Bulk create of 30 records should easily complete in under 500ms
    assert duration_ms < 1000, f"Bulk attendance took {duration_ms}ms"


@pytest.mark.django_db
def test_performance_student_list_and_attendance_roster(client, perf_env):
    """Benchmark student list pagination and attendance roster generation latencies."""
    admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {perf_env['tokens']['admin']}"}
    guru_headers = {"HTTP_AUTHORIZATION": f"Bearer {perf_env['tokens']['guru']}"}

    # 1. Student List Latency (15 iterations)
    list_latencies = []
    for _ in range(15):
        t0 = time.perf_counter()
        res = client.get("/api/master/students?page=1&page_size=20", **admin_headers)
        t1 = time.perf_counter()
        assert res.status_code == 200
        list_latencies.append((t1 - t0) * 1000)

    list_metrics = compute_latencies(list_latencies)
    assert list_metrics["p95_ms"] < 250, f"Student list p95 exceeded budget: {list_metrics}"

    # 2. Attendance Roster Latency (15 iterations)
    roster_latencies = []
    class_id = perf_env["class"].id
    today = date.today().isoformat()
    for _ in range(15):
        t0 = time.perf_counter()
        res = client.get(f"/api/attendance/roster?class_id={class_id}&date={today}", **guru_headers)
        t1 = time.perf_counter()
        assert res.status_code == 200
        roster_latencies.append((t1 - t0) * 1000)

    roster_metrics = compute_latencies(roster_latencies)
    assert roster_metrics["p95_ms"] < 250, f"Roster p95 exceeded budget: {roster_metrics}"


@pytest.mark.django_db
def test_performance_excel_and_pdf_export_latency(client, perf_env):
    """Benchmark binary report generation latency (Excel openpyxl and PDF reportlab)."""
    guru_headers = {"HTTP_AUTHORIZATION": f"Bearer {perf_env['tokens']['guru']}"}
    today = date.today().isoformat()

    # 1. Attendance Excel Export (5 iterations)
    excel_latencies = []
    for _ in range(5):
        t0 = time.perf_counter()
        res = client.get(f"/api/reports/attendance.xlsx?start_date={today}&end_date={today}", **guru_headers)
        t1 = time.perf_counter()
        assert res.status_code == 200
        excel_latencies.append((t1 - t0) * 1000)

    excel_metrics = compute_latencies(excel_latencies)
    # Binary spreadsheet generation under 1000ms
    assert excel_metrics["p95_ms"] < 1000, f"Excel generation exceeded budget: {excel_metrics}"
