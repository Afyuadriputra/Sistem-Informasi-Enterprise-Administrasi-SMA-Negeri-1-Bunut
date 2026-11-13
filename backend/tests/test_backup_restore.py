import hashlib
import shutil
import tempfile
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command

from apps.accounts.models import Role, User, UserRole
from apps.administration.models import Document, ServiceRequest, ServiceType
from apps.master_data.models import AcademicYear, SchoolClass, Student


@pytest.mark.django_db
def test_synthetic_backup_restore_and_checksum_integrity():
    """Verify disaster recovery backup and restore for database and private documents.
    Validates byte-for-byte SHA-256 integrity and database-to-file consistency.
    """
    # 1. Create synthetic data
    ay = AcademicYear.objects.create(name="2026/2027 Backup", start_date="2026-07-01", end_date="2026-12-31")
    SchoolClass.objects.create(academic_year=ay, name="X-Backup", level=10)
    std = Student.objects.create(student_number="99001", name="Siswa Backup", gender="L", status="AKTIF")
    st = ServiceType.objects.create(code="SK-BACKUP", name="Surat Backup", is_active=True)

    tu_role = Role.objects.create(name="Tata Usaha")
    tu_user = User.objects.create_user(username="backup_tu", password="Password123!")
    UserRole.objects.create(user=tu_user, role=tu_role)

    req = ServiceRequest.objects.create(
        request_number="SR-BACKUP-001",
        service_type=st,
        student=std,
        applicant_name="Pemohon Backup",
        purpose="Uji Cadangan",
        status="DIAJUKAN",
        created_by=tu_user,
        version=1,
    )

    # 2. Create physical private file with known content and checksum
    raw_payload = b"%PDF-1.4\nSynthetic Backup Test File Payload %%EOF"
    expected_sha256 = hashlib.sha256(raw_payload).hexdigest()

    storage_key = "backup-test-file-key-uuid-123"
    private_dir = Path(settings.PRIVATE_MEDIA_ROOT)
    private_dir.mkdir(parents=True, exist_ok=True)
    physical_path = private_dir / storage_key
    physical_path.write_bytes(raw_payload)

    doc = Document.objects.create(
        request=req,
        storage_key=storage_key,
        original_filename="arsip_resmi.pdf",
        mime_type="application/pdf",
        file_size=len(raw_payload),
        uploaded_by=tu_user,
    )

    # 3. Perform backup: dumpdata to temporary json file and copy private file
    temp_dir = tempfile.mkdtemp()
    backup_json = Path(temp_dir) / "database_backup.json"
    backup_media_dir = Path(temp_dir) / "media_backup"
    backup_media_dir.mkdir(parents=True, exist_ok=True)

    with open(backup_json, "w", encoding="utf-8") as f:
        call_command(
            "dumpdata",
            "accounts",
            "master_data",
            "administration",
            format="json",
            indent=2,
            stdout=f,
        )

    # Backup media files
    shutil.copy2(physical_path, backup_media_dir / storage_key)

    assert backup_json.exists() and backup_json.stat().st_size > 0
    assert (backup_media_dir / storage_key).exists()

    # 4. Simulate Disaster: delete data and wipe file
    doc_id = doc.id
    Document.objects.all().delete()
    ServiceRequest.objects.all().delete()
    ServiceType.objects.all().delete()
    Student.objects.all().delete()
    SchoolClass.objects.all().delete()
    AcademicYear.objects.all().delete()
    User.objects.filter(username="backup_tu").delete()

    physical_path.unlink()
    assert not physical_path.exists()
    assert Document.objects.filter(id=doc_id).count() == 0

    # 5. Restore: loaddata from backup json and restore physical files
    call_command("loaddata", str(backup_json))
    shutil.copy2(backup_media_dir / storage_key, physical_path)

    # 6. Verify full recovery and integrity
    restored_doc = Document.objects.filter(id=doc_id).first()
    assert restored_doc is not None, "Document record must be fully restored"
    assert restored_doc.original_filename == "arsip_resmi.pdf"
    assert restored_doc.storage_key == storage_key

    assert physical_path.exists(), "Restored physical file must exist on disk"
    restored_bytes = physical_path.read_bytes()
    restored_sha256 = hashlib.sha256(restored_bytes).hexdigest()

    assert restored_sha256 == expected_sha256, "Restored file checksum must match original exactly"
    assert len(restored_bytes) == restored_doc.file_size, "Restored file size must match database record"

    # Cleanup temporary backup directory
    shutil.rmtree(temp_dir, ignore_errors=True)
