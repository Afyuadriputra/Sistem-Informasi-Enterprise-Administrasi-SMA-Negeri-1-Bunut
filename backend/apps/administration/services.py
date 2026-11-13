import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from apps.accounts.models import ActivityLog, User
from apps.administration.models import (
    Document,
    ServiceActionEnum,
    ServiceEvent,
    ServiceRequest,
    ServiceRequestStatusEnum,
    ServiceType,
)
from apps.administration.schemas import (
    ServiceRequestCreateRequest,
    ServiceTransitionRequest,
    ServiceTransitionResponse,
    ServiceTypeCreateRequest,
    ServiceTypeUpdateRequest,
)
from apps.core.exceptions import (
    BusinessValidationError,
    ConcurrencyConflictError,
    NotFoundError,
)
from apps.core.security import require_roles
from apps.master_data.models import Student


@transaction.atomic
def create_service_type(data: ServiceTypeCreateRequest, actor: User) -> ServiceType:
    if ServiceType.objects.filter(code=data.code).exists():
        raise BusinessValidationError(f"Kode jenis layanan '{data.code}' sudah terdaftar.")

    st = ServiceType.objects.create(
        code=data.code,
        name=data.name,
        description=data.description,
        requires_approval=data.requires_approval,
        is_active=data.is_active,
    )
    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_SERVICE_TYPE",
        resource_type="administration",
        resource_id=str(st.id),
    )
    return st


@transaction.atomic
def update_service_type(type_id: int, data: ServiceTypeUpdateRequest, actor: User) -> ServiceType:
    st = ServiceType.objects.filter(id=type_id).first()
    if not st:
        raise NotFoundError("Jenis layanan tidak ditemukan.")

    if data.name is not None:
        st.name = data.name
    if data.description is not None:
        st.description = data.description
    if data.requires_approval is not None:
        st.requires_approval = data.requires_approval
    if data.is_active is not None:
        st.is_active = data.is_active

    st.save()
    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_SERVICE_TYPE",
        resource_type="administration",
        resource_id=str(st.id),
    )
    return st


@transaction.atomic
def create_service_request(
    data: ServiceRequestCreateRequest, actor: User, request_id: Optional[str] = None
) -> ServiceRequest:
    service_type = ServiceType.objects.filter(id=data.service_type_id, is_active=True).first()
    if not service_type:
        raise NotFoundError("Jenis layanan tidak ditemukan atau tidak aktif.")

    student = None
    if data.student_id:
        student = Student.objects.filter(id=data.student_id).first()
        if not student:
            raise NotFoundError("Data siswa pemohon tidak ditemukan.")

    req_number = f"SR-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    req = ServiceRequest.objects.create(
        request_number=req_number,
        service_type=service_type,
        applicant_name=data.applicant_name,
        applicant_phone=data.applicant_phone,
        student=student,
        purpose=data.purpose,
        status=ServiceRequestStatusEnum.DIAJUKAN,
        created_by=actor,
        version=1,
    )

    ServiceEvent.objects.create(
        request=req,
        action="BUAT_PERMOHONAN",
        initial_status=ServiceRequestStatusEnum.DIAJUKAN,
        final_status=ServiceRequestStatusEnum.DIAJUKAN,
        note="Permohonan surat berhasil dibuat.",
        actor=actor,
    )

    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_SERVICE_REQUEST",
        resource_type="administration",
        resource_id=str(req.id),
        request_id=request_id,
        metadata=f'{{"request_number": "{req.request_number}"}}',
    )
    return req


@transaction.atomic
def transition_service_request(
    request_id: int, data: ServiceTransitionRequest, actor: User, request_id_header: Optional[str] = None
) -> ServiceTransitionResponse:
    req = ServiceRequest.objects.select_for_update().select_related("service_type").filter(id=request_id).first()
    if not req:
        raise NotFoundError("Permohonan surat tidak ditemukan.")

    if req.status in (ServiceRequestStatusEnum.DITOLAK, ServiceRequestStatusEnum.SELESAI):
        raise BusinessValidationError(
            f"Permohonan telah berada pada status akhir '{req.status}' dan tidak dapat diubah lagi."
        )

    # Optimistic locking
    if req.version != data.expected_version:
        raise ConcurrencyConflictError(
            message="Data permohonan telah diubah oleh pengguna lain. Silakan muat ulang halaman.",
            details=[{"current_version": req.version, "provided_version": data.expected_version}],
        )

    initial_status = req.status

    if data.action == ServiceActionEnum.PROSES:
        require_roles(actor, ["Administrator", "Tata Usaha"])
        if req.status != ServiceRequestStatusEnum.DIAJUKAN:
            raise BusinessValidationError("Aksi PROSES hanya dapat dilakukan pada permohonan berstatus DIAJUKAN.")
        final_status = ServiceRequestStatusEnum.DIPROSES

    elif data.action == ServiceActionEnum.AJUKAN_PERSETUJUAN:
        require_roles(actor, ["Administrator", "Tata Usaha"])
        if req.status != ServiceRequestStatusEnum.DIPROSES:
            raise BusinessValidationError("Permohonan harus berstatus DIPROSES sebelum diajukan persetujuan.")
        final_status = ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN

    elif data.action == ServiceActionEnum.SETUJUI:
        require_roles(actor, ["Administrator", "Pimpinan"])
        if req.status != ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN:
            raise BusinessValidationError("Hanya permohonan MENUNGGU_PERSETUJUAN yang dapat disetujui.")
        final_status = ServiceRequestStatusEnum.DISETUJUI

    elif data.action == ServiceActionEnum.TOLAK:
        require_roles(actor, ["Administrator", "Pimpinan", "Tata Usaha"])
        if not data.note or not data.note.strip():
            raise BusinessValidationError("Alasan penolakan permohonan wajib diisi.")
        final_status = ServiceRequestStatusEnum.DITOLAK

    elif data.action == ServiceActionEnum.SELESAIKAN:
        require_roles(actor, ["Administrator", "Tata Usaha"])
        if req.service_type.requires_approval:
            if req.status != ServiceRequestStatusEnum.DISETUJUI:
                raise BusinessValidationError("Permohonan memerlukan persetujuan sebelum dapat diselesaikan.")
        else:
            if req.status != ServiceRequestStatusEnum.DIPROSES:
                raise BusinessValidationError("Permohonan harus berstatus DIPROSES sebelum diselesaikan.")
        final_status = ServiceRequestStatusEnum.SELESAI

    else:
        raise BusinessValidationError(f"Aksi transisi '{data.action}' tidak valid.")

    req.status = final_status
    req.version += 1
    req.save()

    ServiceEvent.objects.create(
        request=req,
        action=data.action,
        initial_status=initial_status,
        final_status=final_status,
        note=data.note,
        actor=actor,
    )

    ActivityLog.objects.create(
        actor=actor,
        action="TRANSITION_SERVICE_REQUEST",
        resource_type="administration",
        resource_id=str(req.id),
        request_id=request_id_header,
        metadata=f'{{"action": "{data.action}", "version": {req.version}}}',
    )

    return ServiceTransitionResponse(
        id=req.id,
        status=req.status,
        version=req.version,
        message="Status permohonan berhasil diperbarui.",
    )


@transaction.atomic
def upload_service_document(request_id: int, uploaded_file: UploadedFile, actor: User) -> Document:
    req = ServiceRequest.objects.filter(id=request_id).first()
    if not req:
        raise NotFoundError("Permohonan surat tidak ditemukan.")

    require_roles(actor, ["Administrator", "Tata Usaha"])

    # 1. Size check: max 5 MB (5,242,880 bytes)
    max_size = 5 * 1024 * 1024
    if uploaded_file.size > max_size:
        raise BusinessValidationError("Ukuran berkas melebihi batas maksimum 5 MB.")

    # 2. Extension check
    filename = uploaded_file.name
    ext = Path(filename).suffix.lower()
    allowed_exts = {".pdf", ".jpg", ".jpeg", ".png"}
    if ext not in allowed_exts:
        raise BusinessValidationError("Ekstensi berkas tidak diizinkan. Hanya berkas PDF, JPG, dan PNG yang didukung.")

    # 3. Magic bytes inspection
    header_bytes = uploaded_file.read(16)
    uploaded_file.seek(0)

    mime_type = "application/octet-stream"
    if header_bytes.startswith(b"%PDF-"):
        mime_type = "application/pdf"
    elif header_bytes.startswith(b"\xff\xd8\xff"):
        mime_type = "image/jpeg"
    elif header_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        mime_type = "image/png"
    else:
        raise BusinessValidationError("Format dan struktur isi berkas tidak valid atau tidak sesuai ekstensi.")

    # 4. Save to private storage with random UUID
    storage_key = str(uuid.uuid4())
    private_dir = Path(settings.PRIVATE_MEDIA_ROOT)
    private_dir.mkdir(parents=True, exist_ok=True)
    target_path = private_dir / storage_key

    with open(target_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    doc = Document.objects.create(
        request=req,
        storage_key=storage_key,
        original_filename=filename,
        mime_type=mime_type,
        file_size=uploaded_file.size,
        uploaded_by=actor,
    )

    ActivityLog.objects.create(
        actor=actor,
        action="UPLOAD_PRIVATE_DOCUMENT",
        resource_type="administration",
        resource_id=str(doc.id),
        metadata=f'{{"filename": "{filename}", "size": {doc.file_size}}}',
    )
    return doc
