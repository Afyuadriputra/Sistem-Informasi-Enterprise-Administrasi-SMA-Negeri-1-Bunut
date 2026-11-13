import io
from datetime import date
from pathlib import Path

import pytest
from django.conf import settings
from django.test import Client

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceType
from apps.attendance.models import Attendance, HistoricalAttendance
from apps.master_data.models import (
    AcademicYear,
    ClassAssignment,
    Employee,
    SchoolClass,
    Student,
)
from apps.student_affairs.models import StudentCase


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def e2e_universe(db):
    # 1. Setup Roles
    roles = {
        "admin": Role.objects.create(name="Administrator"),
        "pimpinan": Role.objects.create(name="Pimpinan"),
        "kesiswaan": Role.objects.create(name="Kesiswaan"),
        "tu": Role.objects.create(name="Tata Usaha"),
        "guru": Role.objects.create(name="Guru"),
    }

    # 2. Setup Users
    def make_user(username, role_name):
        u = User.objects.create_user(username=username, password="Password123!")
        UserRole.objects.create(user=u, role=roles[role_name])
        return u

    admin_u = make_user("admin_e2e", "admin")
    kepsek_u = make_user("kepsek_e2e", "pimpinan")
    kesiswaan_u = make_user("kesiswaan_e2e", "kesiswaan")
    tu_u = make_user("tu_e2e", "tu")
    guru1_u = make_user("guru1_e2e", "guru")
    guru2_u = make_user("guru2_e2e", "guru")

    # 3. Setup Employees
    emp1 = Employee.objects.create(user=guru1_u, nip="19800101", name="Guru Satu")
    emp2 = Employee.objects.create(user=guru2_u, nip="19800202", name="Guru Dua")

    # 4. Issue Tokens
    tokens = {
        "admin": issue_token_pair(admin_u)["access_token"],
        "kepsek": issue_token_pair(kepsek_u)["access_token"],
        "kesiswaan": issue_token_pair(kesiswaan_u)["access_token"],
        "tu": issue_token_pair(tu_u)["access_token"],
        "guru1": issue_token_pair(guru1_u)["access_token"],
        "guru2": issue_token_pair(guru2_u)["access_token"],
    }

    return {
        "users": {
            "admin": admin_u,
            "kepsek": kepsek_u,
            "kesiswaan": kesiswaan_u,
            "tu": tu_u,
            "guru1": guru1_u,
            "guru2": guru2_u,
        },
        "employees": {"emp1": emp1, "emp2": emp2},
        "tokens": tokens,
    }


@pytest.mark.django_db
class TestBackendEndToEndScenarios:
    def test_scenario_a_academic_lifecycle_and_attendance(self, client, e2e_universe):
        """Scenario A:
        1. Admin creates Academic Year & Class.
        2. Admin creates Student & Enrolls student into Class.
        3. Admin assigns Guru 1 to Class as GURU_MAPEL.
        4. Guru 1 records bulk attendance.
        5. Historical records snapshot verified in HistoricalAttendance.
        """
        admin_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['admin']}"}
        guru1_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['guru1']}"}

        # 1. Academic Year
        ay_res = client.post(
            "/api/master/academic-years",
            data={
                "name": "2026/2027 Semester Ganjil E2E",
                "start_date": "2026-07-01",
                "end_date": "2026-12-31",
                "is_active": True,
            },
            content_type="application/json",
            **admin_h,
        )
        assert ay_res.status_code == 201
        ay_id = ay_res.json()["id"]

        # Class
        cls_res = client.post(
            "/api/master/classes",
            data={"academic_year_id": ay_id, "name": "XI-IPA-1", "level": 11},
            content_type="application/json",
            **admin_h,
        )
        assert cls_res.status_code == 201
        cls_id = cls_res.json()["id"]

        # 2. Student & Enrollment
        std_res = client.post(
            "/api/master/students",
            data={
                "student_number": "NISN-E2E-001",
                "name": "Rian Pratama",
                "gender": "LAKI_LAKI",
                "status": "AKTIF",
            },
            content_type="application/json",
            **admin_h,
        )
        assert std_res.status_code == 201
        std_id = std_res.json()["id"]

        enr_res = client.post(
            "/api/master/enrollments",
            data={"student_id": std_id, "class_id": cls_id, "start_date": "2026-07-01"},
            content_type="application/json",
            **admin_h,
        )
        assert enr_res.status_code == 201

        # 3. Class Assignment for Guru 1
        emp1_id = e2e_universe["employees"]["emp1"].id
        asgn_res = client.post(
            "/api/master/assignments",
            data={
                "employee_id": emp1_id,
                "class_id": cls_id,
                "role": "GURU_MAPEL",
                "start_date": "2026-07-01",
            },
            content_type="application/json",
            **admin_h,
        )
        assert asgn_res.status_code == 201

        # 4. Guru 1 records bulk attendance
        today_str = date.today().isoformat()
        att_res = client.post(
            "/api/attendance/bulk",
            data={
                "class_id": cls_id,
                "date": today_str,
                "items": [{"student_id": std_id, "status": "HADIR", "note": "Hadir tepat waktu"}],
            },
            content_type="application/json",
            **guru1_h,
        )
        assert att_res.status_code == 200
        assert att_res.json()["saved_count"] == 1

        # 5. Verify database and audit history
        att_obj = Attendance.objects.get(school_class_id=cls_id, student_id=std_id, date=today_str)
        assert att_obj.status == "HADIR"
        history_records = HistoricalAttendance.objects.filter(id=att_obj.id)
        assert history_records.count() >= 1

    def test_scenario_b_student_affairs_case_and_counseling(self, client, e2e_universe):
        """Scenario B:
        1. Kesiswaan reports a student case.
        2. Kesiswaan transitions case: BARU -> DIPROSES with counseling action note.
        3. Kesiswaan records an event on the timeline.
        4. Kesiswaan completes case: DIPROSES -> SELESAI.
        """
        kesiswaan_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['kesiswaan']}"}

        # Setup student
        std = Student.objects.create(student_number="NISN-BK-001", name="Dedi Saputra", gender="LAKI_LAKI")

        # 1. Kesiswaan creates case
        create_res = client.post(
            "/api/student-affairs/cases",
            data={
                "student_id": std.id,
                "title": "Keterlambatan Berulang",
                "summary": "Siswa sering terlambat 30 menit pada jam pertama",
            },
            content_type="application/json",
            **kesiswaan_h,
        )
        assert create_res.status_code == 201
        case_id = create_res.json()["id"]

        # 2. Transition BARU -> DIPROSES
        trans1 = client.post(
            f"/api/student-affairs/cases/{case_id}/transitions",
            data={
                "action": "MULAI_PENANGANAN",
                "expected_version": 1,
                "note": "Memanggil siswa untuk sesi konseling bimbingan",
            },
            content_type="application/json",
            **kesiswaan_h,
        )
        assert trans1.status_code == 200
        assert trans1.json()["status"] == "DIPROSES"
        assert trans1.json()["version"] == 2

        # 3. Add timeline counseling note via CATAT_TINDAKAN transition
        event_res = client.post(
            f"/api/student-affairs/cases/{case_id}/transitions",
            data={
                "action": "CATAT_TINDAKAN",
                "expected_version": 2,
                "note": "Siswa telah menandatangani komitmen kedisiplinan bersama orang tua",
            },
            content_type="application/json",
            **kesiswaan_h,
        )
        assert event_res.status_code == 200
        assert event_res.json()["version"] == 3

        # 4. Transition DIPROSES -> SELESAI
        trans2 = client.post(
            f"/api/student-affairs/cases/{case_id}/transitions",
            data={
                "action": "SELESAIKAN",
                "expected_version": 3,
                "note": "Kasus selesai dengan rekomendasi pemantauan",
            },
            content_type="application/json",
            **kesiswaan_h,
        )
        assert trans2.status_code == 200
        assert trans2.json()["status"] == "SELESAI"
        assert trans2.json()["version"] == 4

    def test_scenario_c_letter_request_upload_approval_download(self, client, e2e_universe):
        """Scenario C:
        1. TU creates service request for student.
        2. TU transitions DIAJUKAN -> DIPROSES.
        3. TU uploads official PDF document (verifying magic bytes & private media path).
        4. TU transitions DIPROSES -> MENUNGGU_PERSETUJUAN.
        5. Kepsek (Pimpinan) transitions MENUNGGU_PERSETUJUAN -> DISETUJUI.
        6. TU transitions DISETUJUI -> SELESAI.
        7. Kepsek downloads private document via protected stream.
        """
        tu_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['tu']}"}
        kepsek_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['kepsek']}"}

        st = ServiceType.objects.create(
            code="SK-LULUS-E2E",
            name="Surat Keterangan Lulus",
            requires_approval=True,
            is_active=True,
        )

        # 1. TU creates request
        req_res = client.post(
            "/api/administration/requests",
            data={
                "service_type_id": st.id,
                "applicant_name": "Ibu Maryam",
                "applicant_phone": "081377889900",
                "purpose": "Pendaftaran perguruan tinggi negeri",
            },
            content_type="application/json",
            **tu_h,
        )
        assert req_res.status_code == 201
        req_id = req_res.json()["id"]

        # 2. Transition -> DIPROSES
        t1 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "PROSES", "expected_version": 1, "note": "Verifikasi berkas persyaratan"},
            content_type="application/json",
            **tu_h,
        )
        assert t1.status_code == 200

        # 3. Upload PDF attachment
        pdf_bytes = io.BytesIO(b"%PDF-1.4\n%Official signed letter content stream\n%%EOF")
        pdf_bytes.name = "draf_skl.pdf"
        up_res = client.post(
            f"/api/administration/requests/{req_id}/documents",
            data={"file": pdf_bytes},
            **tu_h,
        )
        assert up_res.status_code == 201
        doc_data = up_res.json()
        doc_id = doc_data["id"]

        # Check file stored in PRIVATE_MEDIA_ROOT with UUID key
        storage_file = Path(settings.PRIVATE_MEDIA_ROOT) / doc_data["storage_key"]
        assert storage_file.exists()

        # 4. Transition -> MENUNGGU_PERSETUJUAN
        t2 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "AJUKAN_PERSETUJUAN", "expected_version": 2, "note": "Mohon pengesahan Kepala Sekolah"},
            content_type="application/json",
            **tu_h,
        )
        assert t2.status_code == 200

        # 5. Kepsek APPROVES
        t3 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "SETUJUI", "expected_version": 3, "note": "Dokumen telah diverifikasi dan disahkan"},
            content_type="application/json",
            **kepsek_h,
        )
        assert t3.status_code == 200

        # 6. TU finalizes SELESAI
        t4 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "SELESAIKAN", "expected_version": 4, "note": "Surat resmi diserahkan ke pemohon"},
            content_type="application/json",
            **tu_h,
        )
        assert t4.status_code == 200

        # 7. Kepsek downloads document
        dl_res = client.get(f"/api/administration/documents/{doc_id}/download", **kepsek_h)
        assert dl_res.status_code == 200
        assert dl_res["Content-Type"] == "application/pdf"
        dl_content = b"".join(dl_res.streaming_content)
        assert dl_content.startswith(b"%PDF-")

    def test_scenario_d_cross_role_boundary_least_privilege(self, client, e2e_universe):
        """Scenario D: Security & IDOR cross-role boundary enforcement:
        1. Guru attempting to create service requests -> 403.
        2. TU attempting to record attendance -> 403.
        3. Guru 2 attempting to record attendance in Guru 1's class -> 403.
        4. Guru attempting to download private administration documents -> 403.
        5. Non-Admin attempting to query audit logs -> 403.
        """
        guru1_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['guru1']}"}
        guru2_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['guru2']}"}
        tu_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['tu']}"}
        kesiswaan_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['kesiswaan']}"}

        # 1. Guru creates service request -> 403
        r1 = client.post(
            "/api/administration/requests",
            data={"service_type_id": 1, "applicant_name": "Test", "purpose": "Test"},
            content_type="application/json",
            **guru1_h,
        )
        assert r1.status_code == 403

        # 2. TU records attendance -> 403
        ay = AcademicYear.objects.create(name="2026/2027 E2E D", start_date="2026-07-01", end_date="2026-12-31")
        cls_guru1 = SchoolClass.objects.create(academic_year=ay, name="X-1", level=10)
        ClassAssignment.objects.create(
            employee=e2e_universe["employees"]["emp1"],
            school_class=cls_guru1,
            role="GURU_MAPEL",
            start_date="2026-07-01",
        )
        today_str = date.today().isoformat()
        r2 = client.post(
            "/api/attendance/bulk",
            data={"class_id": cls_guru1.id, "date": today_str, "items": []},
            content_type="application/json",
            **tu_h,
        )
        assert r2.status_code == 403

        # 3. Guru 2 records attendance in unassigned class -> 403
        r3 = client.post(
            "/api/attendance/bulk",
            data={"class_id": cls_guru1.id, "date": today_str, "items": []},
            content_type="application/json",
            **guru2_h,
        )
        assert r3.status_code == 403

        # 4. Guru downloads private document -> 403
        r4 = client.get("/api/administration/documents/1/download", **guru1_h)
        assert r4.status_code in (403, 404)

        # 5. Kesiswaan queries audit logs -> 403
        r5 = client.get("/api/audit-logs", **kesiswaan_h)
        assert r5.status_code == 403

    def test_scenario_e_concurrency_race_condition_handling(self, client, e2e_universe):
        """Scenario E: Concurrency conflict detection:
        Mismatched expected_version triggers HTTP 409 Conflict.
        """
        kesiswaan_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['kesiswaan']}"}
        tu_h = {"HTTP_AUTHORIZATION": f"Bearer {e2e_universe['tokens']['tu']}"}

        # Case optimistic locking
        std = Student.objects.create(student_number="NISN-RACE-001", name="Rudi", gender="LAKI_LAKI")
        case = StudentCase.objects.create(
            student=std,
            title="Race condition case",
            summary="Testing optimistic concurrency",
            version=3,
        )

        res_case = client.post(
            f"/api/student-affairs/cases/{case.id}/transitions",
            data={"action": "MULAI_PENANGANAN", "expected_version": 2, "note": "Stale expected version"},
            content_type="application/json",
            **kesiswaan_h,
        )
        assert res_case.status_code == 409
        assert res_case.json()["code"] == "CONCURRENCY_CONFLICT"

        # Service request optimistic locking
        st = ServiceType.objects.create(code="SK-RACE", name="Layanan Race", is_active=True)
        sr = ServiceRequest.objects.create(
            request_number="SR-RACE-001",
            service_type=st,
            applicant_name="Pemohon Stale",
            purpose="Test Concurrency",
            version=5,
            created_by=e2e_universe["users"]["tu"],
        )

        res_sr = client.post(
            f"/api/administration/requests/{sr.id}/transitions",
            data={"action": "PROSES", "expected_version": 4, "note": "Stale version"},
            content_type="application/json",
            **tu_h,
        )
        assert res_sr.status_code == 409
        assert res_sr.json()["code"] == "CONCURRENCY_CONFLICT"
