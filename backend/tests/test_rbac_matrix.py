from datetime import date

import pytest

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceType
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
def rbac_env(db):
    roles = {
        name: Role.objects.create(name=name)
        for name in ["Administrator", "Pimpinan", "Kesiswaan", "Tata Usaha", "Wali Kelas", "Guru"]
    }

    users = {}
    tokens = {}
    for role_name in roles:
        u = User.objects.create_user(username=f"user_{role_name.lower().replace(' ', '_')}", password="Password123!")
        UserRole.objects.create(user=u, role=roles[role_name])
        users[role_name] = u
        tokens[role_name] = issue_token_pair(u)["access_token"]

    # Master Data setup
    ay = AcademicYear.objects.create(
        name="2026/2027 Ganjil", start_date="2026-07-01", end_date="2026-12-31", is_active=True
    )
    cls1 = SchoolClass.objects.create(academic_year=ay, name="X-A", level=10)
    cls2 = SchoolClass.objects.create(academic_year=ay, name="X-B", level=10)
    std1 = Student.objects.create(student_number="1001", name="Siswa A", gender="L", status="AKTIF")
    std2 = Student.objects.create(student_number="1002", name="Siswa B", gender="P", status="AKTIF")

    Enrollment.objects.create(student=std1, school_class=cls1, start_date="2026-07-01")
    Enrollment.objects.create(student=std2, school_class=cls2, start_date="2026-07-01")

    # Wali Kelas assignment to cls1
    emp_wali = Employee.objects.create(user=users["Wali Kelas"], nip="198001", name="Wali Kelas A")
    ClassAssignment.objects.create(employee=emp_wali, school_class=cls1, role="WALI_KELAS", start_date="2026-07-01")

    # Guru assignment to cls1
    emp_guru = Employee.objects.create(user=users["Guru"], nip="198002", name="Guru Mapel A")
    ClassAssignment.objects.create(employee=emp_guru, school_class=cls1, role="GURU_MAPEL", start_date="2026-07-01")

    # Service Request setup
    st = ServiceType.objects.create(code="SK-AKTIF", name="Surat Keterangan Aktif", is_active=True)
    sr = ServiceRequest.objects.create(
        request_number="SR-2026-001",
        service_type=st,
        student=std1,
        applicant_name="Orang Tua",
        purpose="Pengajuan KIP",
        status="MENUNGGU_PERSETUJUAN",
        created_by=users["Tata Usaha"],
        version=1,
    )

    # Student Case setup with private counseling action
    sc = StudentCase.objects.create(
        student=std1,
        title="Kasus Disiplin",
        summary="Pelanggaran tata tertib",
        status=CaseStatusEnum.DIPROSES,
        version=1,
    )
    CaseEvent.objects.create(
        case=sc,
        actor=users["Kesiswaan"],
        action="CATAT_TINDAKAN",
        initial_status=CaseStatusEnum.DIPROSES,
        final_status=CaseStatusEnum.DIPROSES,
        note="Siswa menceritakan masalah keluarga yang sangat rahasia.",
    )

    return {
        "users": users,
        "tokens": tokens,
        "cls1": cls1,
        "cls2": cls2,
        "std1": std1,
        "std2": std2,
        "sr": sr,
        "sc": sc,
        "st": st,
    }


@pytest.mark.django_db
def test_rbac_audit_logs_strictly_administrator_only(client, rbac_env):
    """Verify GET /api/audit-logs is strictly restricted to Administrator."""
    for role_name, token in rbac_env["tokens"].items():
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        res = client.get("/api/audit-logs", **headers)
        if role_name == "Administrator":
            assert res.status_code == 200
        else:
            assert res.status_code == 403, f"{role_name} should be denied access to audit logs"


@pytest.mark.django_db
def test_rbac_service_request_approval_pimpinan_only(client, rbac_env):
    """Verify approving a service request requires role Pimpinan (Administrator denied)."""
    sr_id = rbac_env["sr"].id
    payload = {"action": "SETUJUI", "notes": "Disetujui oleh pejabat berwenang", "expected_version": 1}

    # 1. Administrator attempt -> 403 Forbidden
    admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {rbac_env['tokens']['Administrator']}"}
    res_admin = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data=payload,
        content_type="application/json",
        **admin_headers,
    )
    assert res_admin.status_code == 403, "Administrator must NOT approve service requests directly"

    # 2. Tata Usaha attempt -> 403 Forbidden
    tu_headers = {"HTTP_AUTHORIZATION": f"Bearer {rbac_env['tokens']['Tata Usaha']}"}
    res_tu = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data=payload,
        content_type="application/json",
        **tu_headers,
    )
    assert res_tu.status_code == 403

    # 3. Pimpinan attempt -> 200 OK
    pimpinan_headers = {"HTTP_AUTHORIZATION": f"Bearer {rbac_env['tokens']['Pimpinan']}"}
    res_pimpinan = client.post(
        f"/api/administration/requests/{sr_id}/transitions",
        data=payload,
        content_type="application/json",
        **pimpinan_headers,
    )
    assert res_pimpinan.status_code == 200
    assert res_pimpinan.json()["status"] == "DISETUJUI"


@pytest.mark.django_db
def test_rbac_attendance_bulk_save_permissions(client, rbac_env):
    """Verify saving attendance requires assigned teacher or teacher role; Administrator denied without assignment."""
    cls1_id = rbac_env["cls1"].id
    cls2_id = rbac_env["cls2"].id
    today = date.today().isoformat()

    payload_cls1 = {
        "class_id": cls1_id,
        "date": today,
        "items": [{"student_id": rbac_env["std1"].id, "status": "HADIR", "note": ""}],
    }

    # 1. Standalone Administrator attempt -> 403 Forbidden
    admin_h = {"HTTP_AUTHORIZATION": f"Bearer {rbac_env['tokens']['Administrator']}"}
    res_admin = client.post("/api/attendance/bulk", data=payload_cls1, content_type="application/json", **admin_h)
    assert res_admin.status_code == 403

    # 2. Guru attempt on assigned class -> 200 OK
    guru_h = {"HTTP_AUTHORIZATION": f"Bearer {rbac_env['tokens']['Guru']}"}
    res_guru = client.post("/api/attendance/bulk", data=payload_cls1, content_type="application/json", **guru_h)
    assert res_guru.status_code == 200

    # 3. Guru attempt on unassigned class -> 403 Forbidden
    payload_cls2 = {
        "class_id": cls2_id,
        "date": today,
        "items": [{"student_id": rbac_env["std2"].id, "status": "HADIR", "note": ""}],
    }
    res_unassigned = client.post("/api/attendance/bulk", data=payload_cls2, content_type="application/json", **guru_h)
    assert res_unassigned.status_code == 403


@pytest.mark.django_db
def test_rbac_reports_export_matrix(client, rbac_env):
    """Verify attendance.xlsx and administration.pdf strict role boundaries."""
    today = date.today().isoformat()

    # Attendance export: Guru, Wali Kelas, Kesiswaan, Pimpinan allowed; TU and standalone Admin denied
    for role_name, token in rbac_env["tokens"].items():
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        res = client.get(f"/api/reports/attendance.xlsx?start_date={today}&end_date={today}", **headers)
        if role_name in ["Pimpinan", "Kesiswaan", "Wali Kelas", "Guru"]:
            assert res.status_code == 200, f"{role_name} should be allowed attendance export"
        else:
            assert res.status_code == 403, f"{role_name} should be denied attendance export"

    # Administration export: Tata Usaha and Pimpinan allowed; Admin, Guru, Wali, Kesiswaan denied
    for role_name, token in rbac_env["tokens"].items():
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
        res = client.get(f"/api/reports/administration.pdf?start_date={today}&end_date={today}", **headers)
        if role_name in ["Tata Usaha", "Pimpinan"]:
            assert res.status_code == 200, f"{role_name} should be allowed administration export"
        else:
            assert res.status_code == 403, f"{role_name} should be denied administration export"
