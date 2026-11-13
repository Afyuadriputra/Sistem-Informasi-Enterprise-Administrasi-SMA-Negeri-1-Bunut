import io
from pathlib import Path

import pytest
from django.conf import settings
from django.test import Client

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import ServiceRequest, ServiceRequestStatusEnum, ServiceType


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_setup(db):
    admin_r = Role.objects.create(name="Administrator")
    tu_r = Role.objects.create(name="Tata Usaha")
    pimpinan_r = Role.objects.create(name="Pimpinan")
    guru_r = Role.objects.create(name="Guru")

    tu_user = User.objects.create_user(username="tu_staff", password="Password123!")
    UserRole.objects.create(user=tu_user, role=tu_r)

    pimpinan_user = User.objects.create_user(username="kepsek", password="Password123!")
    UserRole.objects.create(user=pimpinan_user, role=pimpinan_r)

    guru_user = User.objects.create_user(username="guru_budi", password="Password123!")
    UserRole.objects.create(user=guru_user, role=guru_r)

    admin_user = User.objects.create_user(username="admin_sys", password="Password123!")
    UserRole.objects.create(user=admin_user, role=admin_r)

    st = ServiceType.objects.create(
        code="SK-AKTIF",
        name="Surat Keterangan Aktif",
        description="Surat keterangan siswa aktif sekolah",
        requires_approval=True,
        is_active=True,
    )

    return {
        "tu_token": issue_token_pair(tu_user)["access_token"],
        "pimpinan_token": issue_token_pair(pimpinan_user)["access_token"],
        "guru_token": issue_token_pair(guru_user)["access_token"],
        "admin_token": issue_token_pair(admin_user)["access_token"],
        "tu_user": tu_user,
        "service_type": st,
    }


@pytest.mark.django_db
class TestAdministrationModule:
    def test_create_and_list_service_types(self, client, admin_setup):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['tu_token']}"}

        # List types
        res = client.get("/api/administration/service-types", **headers)
        assert res.status_code == 200
        data = res.json()
        assert "items" in data
        assert len(data["items"]) >= 1

        # Create type
        payload = {
            "code": "SK-PINDAH",
            "name": "Surat Pindah Sekolah",
            "description": "Surat keterangan pindah sekolah",
            "requires_approval": True,
            "is_active": True,
        }
        res_create = client.post(
            "/api/administration/service-types",
            data=payload,
            content_type="application/json",
            **headers,
        )
        assert res_create.status_code == 201
        assert res_create.json()["code"] == "SK-PINDAH"

    def test_service_request_lifecycle(self, client, admin_setup):
        tu_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['tu_token']}"}
        pimpinan_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['pimpinan_token']}"}
        st = admin_setup["service_type"]

        # 1. TU creates request (DIAJUKAN)
        req_payload = {
            "service_type_id": st.id,
            "applicant_name": "Ahmad Dani",
            "applicant_phone": "081234567890",
            "purpose": "Keperluan beasiswa Pemda",
        }
        res_create = client.post(
            "/api/administration/requests",
            data=req_payload,
            content_type="application/json",
            **tu_headers,
        )
        assert res_create.status_code == 201
        req_data = res_create.json()
        req_id = req_data["id"]
        assert req_data["status"] == ServiceRequestStatusEnum.DIAJUKAN
        assert req_data["version"] == 1

        # 2. TU processes request (DIPROSES)
        res_trans1 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "PROSES", "expected_version": 1, "note": "Mulai diproses TU"},
            content_type="application/json",
            **tu_headers,
        )
        assert res_trans1.status_code == 200
        assert res_trans1.json()["status"] == ServiceRequestStatusEnum.DIPROSES
        assert res_trans1.json()["version"] == 2

        # 3. TU submits for approval (MENUNGGU_PERSETUJUAN)
        res_trans2 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "AJUKAN_PERSETUJUAN", "expected_version": 2, "note": "Mohon ditandatangani Kepala Sekolah"},
            content_type="application/json",
            **tu_headers,
        )
        assert res_trans2.status_code == 200
        assert res_trans2.json()["status"] == ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN
        assert res_trans2.json()["version"] == 3

        # 4. Pimpinan approves (DISETUJUI)
        res_trans3 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "SETUJUI", "expected_version": 3, "note": "Disetujui dan ditandatangani digital"},
            content_type="application/json",
            **pimpinan_headers,
        )
        assert res_trans3.status_code == 200
        assert res_trans3.json()["status"] == ServiceRequestStatusEnum.DISETUJUI
        assert res_trans3.json()["version"] == 4

        # 5. TU finalizes (SELESAI)
        res_trans4 = client.post(
            f"/api/administration/requests/{req_id}/transitions",
            data={"action": "SELESAIKAN", "expected_version": 4, "note": "Surat fisik diserahkan kepada pemohon"},
            content_type="application/json",
            **tu_headers,
        )
        assert res_trans4.status_code == 200
        assert res_trans4.json()["status"] == ServiceRequestStatusEnum.SELESAI
        assert res_trans4.json()["version"] == 5

    def test_be_06_optimistic_concurrency_conflict(self, client, admin_setup):
        tu_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['tu_token']}"}
        st = admin_setup["service_type"]
        tu_user = admin_setup["tu_user"]
        req = ServiceRequest.objects.create(
            request_number="SR-TEST-001",
            service_type=st,
            applicant_name="Rina",
            purpose="Surat riset",
            status=ServiceRequestStatusEnum.DIAJUKAN,
            version=2,
            created_by=tu_user,
        )

        # Mismatched expected_version
        res = client.post(
            f"/api/administration/requests/{req.id}/transitions",
            data={"action": "PROSES", "expected_version": 1, "note": "Stale version"},
            content_type="application/json",
            **tu_headers,
        )
        assert res.status_code == 409
        body = res.json()
        assert body["code"] == "CONCURRENCY_CONFLICT"

    def test_be_07_file_upload_validation(self, client, admin_setup):
        tu_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['tu_token']}"}
        st = admin_setup["service_type"]
        tu_user = admin_setup["tu_user"]
        req = ServiceRequest.objects.create(
            request_number="SR-TEST-002",
            service_type=st,
            applicant_name="Bambang",
            purpose="Surat izin",
            status=ServiceRequestStatusEnum.DIPROSES,
            version=1,
            created_by=tu_user,
        )

        # 1. Invalid extension: .exe
        exe_file = io.BytesIO(b"MZ executable header dummy content")
        exe_file.name = "malicious.exe"
        res_exe = client.post(
            f"/api/administration/requests/{req.id}/documents",
            data={"file": exe_file},
            **tu_headers,
        )
        assert res_exe.status_code == 422
        assert "Ekstensi berkas tidak diizinkan" in res_exe.json()["message"]

        # 2. Invalid magic bytes: .pdf extension with fake text content
        fake_pdf = io.BytesIO(b"Not a real PDF file header")
        fake_pdf.name = "fake.pdf"
        res_fake = client.post(
            f"/api/administration/requests/{req.id}/documents",
            data={"file": fake_pdf},
            **tu_headers,
        )
        assert res_fake.status_code == 422
        assert "Format dan struktur isi berkas tidak valid" in res_fake.json()["message"]

        # 3. Valid PDF with real magic bytes (%PDF-1.4)
        valid_pdf = io.BytesIO(b"%PDF-1.4\n%Fake valid test pdf stream content")
        valid_pdf.name = "lampiran_resmi.pdf"
        res_valid = client.post(
            f"/api/administration/requests/{req.id}/documents",
            data={"file": valid_pdf},
            **tu_headers,
        )
        assert res_valid.status_code == 201
        doc_data = res_valid.json()
        assert doc_data["mime_type"] == "application/pdf"
        assert doc_data["original_filename"] == "lampiran_resmi.pdf"

        # Check storage file exists in PRIVATE_MEDIA_ROOT with UUID key
        storage_file = Path(settings.PRIVATE_MEDIA_ROOT) / doc_data["storage_key"]
        assert storage_file.exists()

    def test_be_08_private_document_authorization_download(self, client, admin_setup):
        tu_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['tu_token']}"}
        pimpinan_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['pimpinan_token']}"}
        guru_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_setup['guru_token']}"}
        st = admin_setup["service_type"]

        tu_user = admin_setup["tu_user"]
        req = ServiceRequest.objects.create(
            request_number="SR-TEST-003",
            service_type=st,
            applicant_name="Citra",
            purpose="Surat keterangan",
            status=ServiceRequestStatusEnum.DIPROSES,
            version=1,
            created_by=tu_user,
        )

        # Upload valid file
        valid_png = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDRtestcontent")
        valid_png.name = "kartu_keluarga.png"
        res_upload = client.post(
            f"/api/administration/requests/{req.id}/documents",
            data={"file": valid_png},
            **tu_headers,
        )
        assert res_upload.status_code == 201
        doc_id = res_upload.json()["id"]

        # 1. Guru Mapel downloads -> 403 Forbidden
        res_guru = client.get(f"/api/administration/documents/{doc_id}/download", **guru_headers)
        assert res_guru.status_code == 403

        # 2. Pimpinan downloads -> 200 OK (streaming)
        res_pimpinan = client.get(f"/api/administration/documents/{doc_id}/download", **pimpinan_headers)
        assert res_pimpinan.status_code == 200
        assert res_pimpinan["Content-Type"] == "image/png"

        # 3. Tata Usaha downloads -> 200 OK
        res_tu = client.get(f"/api/administration/documents/{doc_id}/download", **tu_headers)
        assert res_tu.status_code == 200
