from datetime import date

import pytest
from django.core.cache import cache
from django.db import connection
from django.test.utils import CaptureQueriesContext

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceType
from apps.attendance.models import Attendance
from apps.master_data.models import (
    AcademicYear,
    Enrollment,
    SchoolClass,
    Student,
)
from apps.student_affairs.models import CaseStatusEnum, StudentCase


@pytest.fixture
def query_env(db):
    cache.clear()
    roles = {
        name: Role.objects.create(name=name)
        for name in ["Administrator", "Pimpinan", "Kesiswaan", "Tata Usaha", "Guru"]
    }

    u_admin = User.objects.create_user(username="qo_admin", password="Password123!")
    UserRole.objects.create(user=u_admin, role=roles["Administrator"])

    u_tu = User.objects.create_user(username="qo_tu", password="Password123!")
    UserRole.objects.create(user=u_tu, role=roles["Tata Usaha"])

    u_kes = User.objects.create_user(username="qo_kes", password="Password123!")
    UserRole.objects.create(user=u_kes, role=roles["Kesiswaan"])

    u_pim = User.objects.create_user(username="qo_pim", password="Password123!")
    UserRole.objects.create(user=u_pim, role=roles["Pimpinan"])

    tokens = {
        "admin": issue_token_pair(u_admin)["access_token"],
        "tu": issue_token_pair(u_tu)["access_token"],
        "kes": issue_token_pair(u_kes)["access_token"],
        "pim": issue_token_pair(u_pim)["access_token"],
    }

    ay = AcademicYear.objects.create(name="2026/2027", start_date="2026-07-01", end_date="2026-12-31", is_active=True)
    cls1 = SchoolClass.objects.create(academic_year=ay, name="X-1", level=10)

    # Populate 25 students with enrollments
    students = [
        Student(student_number=f"2026{i:03d}", name=f"Siswa {i}", gender="L" if i % 2 == 0 else "P", status="AKTIF")
        for i in range(1, 26)
    ]
    Student.objects.bulk_create(students)
    all_students = list(Student.objects.all())

    enrollments = [Enrollment(student=s, school_class=cls1, start_date="2026-07-01") for s in all_students]
    Enrollment.objects.bulk_create(enrollments)

    # Populate 15 service requests
    st = ServiceType.objects.create(code="SK-QO", name="Surat QO", is_active=True)
    requests = [
        ServiceRequest(
            request_number=f"SR-QO-{i:03d}",
            service_type=st,
            student=all_students[i],
            applicant_name=f"Pemohon {i}",
            purpose="Tujuan",
            status="DIAJUKAN",
            created_by=u_tu,
            version=1,
        )
        for i in range(15)
    ]
    ServiceRequest.objects.bulk_create(requests)

    # Populate 15 student cases
    cases = [
        StudentCase(
            student=all_students[i],
            title=f"Kasus {i}",
            summary="Ringkasan",
            status=CaseStatusEnum.BARU,
            version=1,
        )
        for i in range(15)
    ]
    StudentCase.objects.bulk_create(cases)

    # Populate 25 attendance records for today
    today = date.today()
    attendances = [
        Attendance(
            student=all_students[i],
            school_class=cls1,
            date=today,
            status="H",
            recorded_by=u_admin,
        )
        for i in range(25)
    ]
    Attendance.objects.bulk_create(attendances)

    return {
        "tokens": tokens,
        "class": cls1,
    }


@pytest.mark.django_db
def test_students_list_query_count_no_n_plus_one(client, query_env):
    """Listing 20 students must use constant number of queries (select_related/prefetch_related)."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {query_env['tokens']['admin']}"}
    with CaptureQueriesContext(connection) as ctx:
        res = client.get("/api/master/students?page_size=20", **headers)

    assert res.status_code == 200
    assert len(res.json()["items"]) == 20
    # Queries should be <= 5 (count + data with relations + auth queries)
    assert len(ctx) <= 5, f"Expected <= 5 queries, got {len(ctx)}"


@pytest.mark.django_db
def test_student_cases_list_query_count(client, query_env):
    """Listing 15 student cases must not execute N+1 queries for students or timelines."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {query_env['tokens']['kes']}"}
    with CaptureQueriesContext(connection) as ctx:
        res = client.get("/api/student-affairs/cases?page_size=15", **headers)

    assert res.status_code == 200
    assert len(res.json()["items"]) == 15
    assert len(ctx) <= 6, f"Expected <= 6 queries, got {len(ctx)}"


@pytest.mark.django_db
def test_service_requests_list_query_count(client, query_env):
    """Listing 15 service requests must not execute N+1 queries for service_type or student."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {query_env['tokens']['tu']}"}
    with CaptureQueriesContext(connection) as ctx:
        res = client.get("/api/administration/requests?page_size=15", **headers)

    assert res.status_code == 200
    assert len(res.json()["items"]) == 15
    assert len(ctx) <= 6, f"Expected <= 6 queries, got {len(ctx)}"


@pytest.mark.django_db
def test_attendance_recap_query_count(client, query_env):
    """Attendance recap listing 25 records must not execute N+1 queries."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {query_env['tokens']['pim']}"}
    today = date.today().isoformat()
    with CaptureQueriesContext(connection) as ctx:
        res = client.get(f"/api/attendance?date={today}&class_id={query_env['class'].id}", **headers)

    assert res.status_code == 200
    assert len(res.json()["student_recaps"]) == 25
    assert len(ctx) <= 10, f"Expected <= 10 queries, got {len(ctx)}"


@pytest.mark.django_db
def test_dashboard_metrics_warm_cache_zero_database_queries(client, query_env):
    """Cold cache computes and caches metrics; warm cache executes zero DB queries for metrics."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {query_env['tokens']['pim']}"}

    # Cold cache: executes queries and caches
    res_cold = client.get("/api/reports/dashboard", **headers)
    assert res_cold.status_code == 200

    # Warm cache: user auth queries occur, but zero queries on domain models (Student, Attendance, etc.)
    with CaptureQueriesContext(connection) as ctx:
        res_warm = client.get("/api/reports/dashboard", **headers)

    assert res_warm.status_code == 200
    # At most 2 auth-related queries (user + role), zero domain queries!
    queries_sql = [q["sql"] for q in ctx]
    domain_tables = ["student", "attendance", "service", "case"]
    domain_queries = [sql for sql in queries_sql if any(table in sql.lower() for table in domain_tables)]
    assert len(domain_queries) == 0, f"Expected 0 domain queries on warm cache, found: {domain_queries}"
