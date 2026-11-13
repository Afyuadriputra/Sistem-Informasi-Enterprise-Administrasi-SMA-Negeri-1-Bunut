import io
from datetime import date, timedelta

import openpyxl
import pytest
from django.core.cache import cache
from django.test import Client

from apps.accounts.models import ActivityLog, Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceRequestStatusEnum, ServiceType
from apps.attendance.models import Attendance, AttendanceStatusEnum
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Employee,
    Enrollment,
    SchoolClass,
    Student,
)
from apps.student_affairs.models import CaseStatusEnum, StudentCase


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def reports_setup(db):
    cache.clear()

    # Roles
    admin_r = Role.objects.create(name="Administrator")
    pimpinan_r = Role.objects.create(name="Pimpinan")
    Role.objects.create(name="Kesiswaan")
    tu_r = Role.objects.create(name="Tata Usaha")
    guru_r = Role.objects.create(name="Guru")

    # Users
    admin_u = User.objects.create_user(username="admin_rep", password="Password123!")
    UserRole.objects.create(user=admin_u, role=admin_r)

    pimpinan_u = User.objects.create_user(username="kepsek_rep", password="Password123!")
    UserRole.objects.create(user=pimpinan_u, role=pimpinan_r)

    tu_u = User.objects.create_user(username="tu_rep", password="Password123!")
    UserRole.objects.create(user=tu_u, role=tu_r)

    guru_u = User.objects.create_user(username="guru_rep", password="Password123!")
    UserRole.objects.create(user=guru_u, role=guru_r)

    emp = Employee.objects.create(user=guru_u, nip="19850101", name="Guru Laporan")

    # Master Data
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-01", end_date="2026-12-31", is_active=True
    )
    cls1 = SchoolClass.objects.create(academic_year=ay, name="X-MIPA-1", level=10)
    cls2 = SchoolClass.objects.create(academic_year=ay, name="X-MIPA-2", level=10)

    # Assign Guru to cls1 only
    ClassAssignment.objects.create(
        employee=emp, school_class=cls1, role="GURU_MAPEL", start_date="2026-07-01"
    )

    # Students
    std1 = Student.objects.create(student_number="S001", name="Siswa Satu", gender="LAKI_LAKI", status="AKTIF")
    std2 = Student.objects.create(student_number="S002", name="Siswa Dua", gender="PEREMPUAN", status="AKTIF")
    Enrollment.objects.create(student=std1, school_class=cls1, start_date="2026-07-01")
    Enrollment.objects.create(student=std2, school_class=cls2, start_date="2026-07-01")

    # Attendance today
    today = date.today()
    Attendance.objects.create(
        student=std1,
        school_class=cls1,
        date=today,
        status=AttendanceStatusEnum.HADIR,
        recorded_by=admin_u,
    )

    # Student Case
    StudentCase.objects.create(
        student=std1,
        title="Terlambat Upacara",
        summary="Terlambat 15 menit",
        status=CaseStatusEnum.BARU,
        version=1,
    )

    # Service Request
    st = ServiceType.objects.create(code="SK-AKTIF", name="Surat Keterangan Aktif", is_active=True)
    ServiceRequest.objects.create(
        request_number="SR-REP-001",
        service_type=st,
        applicant_name="Wali Siswa",
        purpose="Pengajuan beasiswa",
        status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
        created_by=tu_u,
    )

    # Activity Log
    ActivityLog.objects.create(
        actor=admin_u,
        action="LOGIN_SUCCESS",
        resource_type="accounts",
    )

    return {
        "admin_token": issue_token_pair(admin_u)["access_token"],
        "pimpinan_token": issue_token_pair(pimpinan_u)["access_token"],
        "tu_token": issue_token_pair(tu_u)["access_token"],
        "guru_token": issue_token_pair(guru_u)["access_token"],
        "cls1": cls1,
        "cls2": cls2,
        "st": st,
    }


@pytest.mark.django_db
class TestReportsModule:
    def test_be_09_dashboard_metrics_role_scoping_and_cache(self, client, reports_setup):
        admin_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['admin_token']}"}
        pimpinan_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['pimpinan_token']}"}
        tu_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['tu_token']}"}
        guru_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['guru_token']}"}

        # 1. Admin metrics
        res_admin = client.get("/api/reports/dashboard", **admin_h)
        assert res_admin.status_code == 200
        data_admin = res_admin.json()
        assert data_admin["role_scope"] == "Administrator"
        assert data_admin["metrics"]["active_students_count"] == 2
        assert data_admin["metrics"]["pending_cases_count"] == 1
        assert data_admin["metrics"]["pending_requests_count"] == 1
        assert data_admin["metrics"]["attendance_summary"]["recorded_today"] is True
        assert data_admin["metrics"]["attendance_summary"]["attendance_rate_pct"] == 100.0

        # 2. Pimpinan metrics (sees pending approval requests)
        res_pimpinan = client.get("/api/reports/dashboard", **pimpinan_h)
        assert res_pimpinan.status_code == 200
        data_pimpinan = res_pimpinan.json()
        assert data_pimpinan["role_scope"] == "Pimpinan"
        assert data_pimpinan["metrics"]["pending_requests_count"] == 1

        # 3. Tata Usaha metrics (no attendance summary)
        res_tu = client.get("/api/reports/dashboard", **tu_h)
        assert res_tu.status_code == 200
        data_tu = res_tu.json()
        assert data_tu["role_scope"] == "Tata Usaha"
        assert data_tu["metrics"]["attendance_summary"] is None
        assert data_tu["metrics"]["pending_requests_count"] == 1

        # 4. Guru metrics (only sees assigned class students: std1 in cls1 -> 1 student)
        res_guru = client.get("/api/reports/dashboard", **guru_h)
        assert res_guru.status_code == 200
        data_guru = res_guru.json()
        assert data_guru["role_scope"] == "Guru"
        assert data_guru["metrics"]["active_students_count"] == 1

        # 5. Verify caching returns fast identical response
        res_cached = client.get("/api/reports/dashboard", **admin_h)
        assert res_cached.status_code == 200
        assert res_cached.json()["role_scope"] == "Administrator"

    def test_be_10_attendance_excel_export(self, client, reports_setup):
        admin_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['admin_token']}"}
        guru_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['guru_token']}"}
        tu_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['tu_token']}"}

        today_str = date.today().isoformat()

        # 1. Tata Usaha attempt -> 403 Forbidden
        res_tu = client.get(
            f"/api/reports/attendance.xlsx?start_date={today_str}&end_date={today_str}",
            **tu_h,
        )
        assert res_tu.status_code == 403

        # 2. Guru attempt on unassigned class (cls2) -> 403 Forbidden
        cls2_id = reports_setup["cls2"].id
        res_guru_cls2 = client.get(
            f"/api/reports/attendance.xlsx?start_date={today_str}&end_date={today_str}&class_id={cls2_id}",
            **guru_h,
        )
        assert res_guru_cls2.status_code == 403

        # 3. Guru attempt on assigned class (cls1) -> 200 OK Excel binary
        cls1_id = reports_setup["cls1"].id
        res_guru_cls1 = client.get(
            f"/api/reports/attendance.xlsx?start_date={today_str}&end_date={today_str}&class_id={cls1_id}",
            **guru_h,
        )
        assert res_guru_cls1.status_code == 200
        assert (
            res_guru_cls1["Content-Type"]
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # Parse Excel bytes
        excel_wb = openpyxl.load_workbook(io.BytesIO(res_guru_cls1.content))
        sheet = excel_wb.active
        assert sheet.title == "Rekap Kehadiran"

        # 4. Admin attempt all classes -> 200 OK
        res_admin = client.get(
            f"/api/reports/attendance.xlsx?start_date={today_str}&end_date={today_str}",
            **admin_h,
        )
        assert res_admin.status_code == 200

    def test_be_10_administration_pdf_export(self, client, reports_setup):
        admin_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['admin_token']}"}
        tu_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['tu_token']}"}
        guru_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['guru_token']}"}

        today_str = date.today().isoformat()
        start_str = (date.today() - timedelta(days=30)).isoformat()

        # 1. Guru attempt -> 403 Forbidden
        res_guru = client.get(
            f"/api/reports/administration.pdf?start_date={start_str}&end_date={today_str}",
            **guru_h,
        )
        assert res_guru.status_code == 403

        # 2. TU attempt -> 200 OK PDF binary
        res_tu = client.get(
            f"/api/reports/administration.pdf?start_date={start_str}&end_date={today_str}",
            **tu_h,
        )
        assert res_tu.status_code == 200
        assert res_tu["Content-Type"] == "application/pdf"
        assert res_tu.content.startswith(b"%PDF-")

        # 3. Admin attempt -> 200 OK PDF binary
        res_admin = client.get(
            f"/api/reports/administration.pdf?start_date={start_str}&end_date={today_str}",
            **admin_h,
        )
        assert res_admin.status_code == 200
        assert res_admin.content.startswith(b"%PDF-")

    def test_audit_logs_query_and_filtering(self, client, reports_setup):
        admin_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['admin_token']}"}
        guru_h = {"HTTP_AUTHORIZATION": f"Bearer {reports_setup['guru_token']}"}

        # 1. Non-admin attempt -> 403 Forbidden
        res_guru = client.get("/api/audit-logs", **guru_h)
        assert res_guru.status_code == 403

        # 2. Admin attempt -> 200 OK with list of logs
        res_admin = client.get("/api/audit-logs", **admin_h)
        assert res_admin.status_code == 200
        data = res_admin.json()
        assert "items" in data
        assert data["total"] >= 1

        # 3. Filter by action
        res_filtered = client.get("/api/audit-logs?action=LOGIN_SUCCESS", **admin_h)
        assert res_filtered.status_code == 200
        filtered_data = res_filtered.json()
        assert len(filtered_data["items"]) >= 1
        assert all(item["action"] == "LOGIN_SUCCESS" for item in filtered_data["items"])
