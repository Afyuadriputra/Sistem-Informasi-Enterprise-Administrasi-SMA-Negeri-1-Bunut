import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.administration.models import Document, ServiceRequest, ServiceType
from apps.master_data.models import AcademicYear, SchoolClass, Student


@pytest.fixture
def files_env(db):
    roles = {name: Role.objects.create(name=name) for name in ["Administrator", "Pimpinan", "Tata Usaha", "Guru"]}

    users = {}
    tokens = {}
    for role_name in roles:
        u = User.objects.create_user(username=f"pf_{role_name.lower().replace(' ', '_')}", password="Password123!")
        UserRole.objects.create(user=u, role=roles[role_name])
        users[role_name] = u
        tokens[role_name] = issue_token_pair(u)["access_token"]

    ay = AcademicYear.objects.create(name="2026/2027", start_date="2026-07-01", end_date="2026-12-31", is_active=True)
    SchoolClass.objects.create(academic_year=ay, name="X-1", level=10)
    std = Student.objects.create(student_number="10090", name="Siswa File", gender="L", status="AKTIF")
    st = ServiceType.objects.create(code="SK-FILE", name="Surat Berkas", is_active=True)

    sr = ServiceRequest.objects.create(
        request_number="SR-FILE-001",
        service_type=st,
        student=std,
        applicant_name="Pemohon File",
        purpose="Uji lampiran",
        status="DIAJUKAN",
        created_by=users["Tata Usaha"],
        version=1,
    )

    return {
        "users": users,
        "tokens": tokens,
        "request": sr,
    }


@pytest.mark.django_db
def test_upload_empty_file_rejected(client, files_env):
    """Uploading a 0-byte file must be rejected with 422."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Tata Usaha']}"}
    empty_file = SimpleUploadedFile("empty.pdf", b"", content_type="application/pdf")

    res = client.post(
        f"/api/administration/requests/{files_env['request'].id}/documents",
        data={"file": empty_file, "document_type": "KTP"},
        **headers,
    )
    assert res.status_code == 422
    assert "tidak boleh kosong" in res.json()["message"].lower()


@pytest.mark.django_db
def test_upload_path_traversal_sanitization(client, files_env):
    """Filenames with directory traversal sequences must be safely sanitized."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Tata Usaha']}"}
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    traversal_file = SimpleUploadedFile("../../etc/passwd.pdf", pdf_content, content_type="application/pdf")

    res = client.post(
        f"/api/administration/requests/{files_env['request'].id}/documents",
        data={"file": traversal_file, "document_type": "KK"},
        **headers,
    )
    assert res.status_code == 201
    doc_id = res.json()["id"]

    # Verify stored file name does NOT contain directory traversal
    doc = Document.objects.get(id=doc_id)
    assert ".." not in doc.storage_key
    assert doc.original_filename == "passwd.pdf"


@pytest.mark.django_db
def test_upload_magic_bytes_mismatch_rejected(client, files_env):
    """Uploading an executable disguised as PDF must be rejected with 422."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Tata Usaha']}"}
    fake_pdf = SimpleUploadedFile("malicious.pdf", b"MZ\x90\x00\x03\x00\x00\x00", content_type="application/pdf")

    res = client.post(
        f"/api/administration/requests/{files_env['request'].id}/documents",
        data={"file": fake_pdf, "document_type": "KTP"},
        **headers,
    )
    assert res.status_code == 422
    assert "tidak sesuai ekstensi" in res.json()["message"].lower()


@pytest.mark.django_db
def test_upload_oversized_file_rejected(client, files_env):
    """Files exceeding 5MB must be rejected with 422."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Tata Usaha']}"}
    large_content = b"%PDF-1.4\n" + b"0" * (5 * 1024 * 1024 + 100)
    large_file = SimpleUploadedFile("large.pdf", large_content, content_type="application/pdf")

    res = client.post(
        f"/api/administration/requests/{files_env['request'].id}/documents",
        data={"file": large_file, "document_type": "IJAZAH"},
        **headers,
    )
    assert res.status_code == 422
    assert "maksimum 5 mb" in res.json()["message"].lower()


@pytest.mark.django_db
def test_download_document_rbac_boundaries(client, files_env):
    """Only Tata Usaha and Pimpinan may download documents; Admin and Guru are denied."""
    # 1. Upload valid document by TU
    tu_headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Tata Usaha']}"}
    valid_pdf = SimpleUploadedFile(
        "surat_pengantar.pdf",
        b"%PDF-1.5 valid sample pdf content %%EOF",
        content_type="application/pdf",
    )
    res_up = client.post(
        f"/api/administration/requests/{files_env['request'].id}/documents",
        data={"file": valid_pdf, "document_type": "KTP"},
        **tu_headers,
    )
    assert res_up.status_code == 201
    doc_id = res_up.json()["id"]

    # 2. TU download -> 200 OK
    res_tu_dl = client.get(f"/api/administration/documents/{doc_id}/download", **tu_headers)
    assert res_tu_dl.status_code == 200
    file_bytes = b"".join(res_tu_dl.streaming_content)
    assert file_bytes.startswith(b"%PDF-")

    # 3. Pimpinan download -> 200 OK
    pimpinan_headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Pimpinan']}"}
    res_pim_dl = client.get(f"/api/administration/documents/{doc_id}/download", **pimpinan_headers)
    assert res_pim_dl.status_code == 200

    # 4. Administrator attempt -> 403 Forbidden
    admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Administrator']}"}
    res_admin_dl = client.get(f"/api/administration/documents/{doc_id}/download", **admin_headers)
    assert res_admin_dl.status_code == 403

    # 5. Guru attempt -> 403 Forbidden
    guru_headers = {"HTTP_AUTHORIZATION": f"Bearer {files_env['tokens']['Guru']}"}
    res_guru_dl = client.get(f"/api/administration/documents/{doc_id}/download", **guru_headers)
    assert res_guru_dl.status_code == 403


@pytest.mark.django_db
def test_upload_failure_triggers_orphan_file_cleanup(client, files_env, monkeypatch):
    """When database write fails after file creation, orphaned file on disk must be unlinked."""
    from pathlib import Path

    from django.conf import settings

    from apps.administration.services import upload_service_document

    tu_user = files_env["users"]["Tata Usaha"]
    sr_id = files_env["request"].id

    valid_file = SimpleUploadedFile("test_orphan.pdf", b"%PDF-1.4 sample content %%EOF", content_type="application/pdf")

    # Monkeypatch Document.objects.create to simulate database error after file writing
    def mock_create(*args, **kwargs):
        raise RuntimeError("Database connection lost during document insert")

    monkeypatch.setattr(Document.objects, "create", mock_create)

    with pytest.raises(RuntimeError):
        upload_service_document(sr_id, valid_file, tu_user)

    # Verify no stray files remain in PRIVATE_MEDIA_ROOT matching the uploaded content
    private_dir = Path(settings.PRIVATE_MEDIA_ROOT)
    for p in private_dir.iterdir():
        if p.is_file():
            assert p.read_bytes() != b"%PDF-1.4 sample content %%EOF"
