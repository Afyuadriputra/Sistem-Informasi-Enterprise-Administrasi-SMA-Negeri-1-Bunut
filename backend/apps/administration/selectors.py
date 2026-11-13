from pathlib import Path
from typing import Optional, Tuple

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

from apps.accounts.models import User
from apps.administration.models import Document, ServiceRequest, ServiceType
from apps.administration.schemas import (
    DocumentItem,
    DocumentListResponse,
    ServiceEventItem,
    ServiceRequestDetailResponse,
    ServiceRequestItem,
    ServiceRequestListResponse,
    ServiceTypeItem,
    ServiceTypeListResponse,
)
from apps.core.exceptions import NotFoundError
from apps.core.security import require_roles


def list_service_types(include_inactive: bool = False) -> ServiceTypeListResponse:
    qs = ServiceType.objects.all()
    if not include_inactive:
        qs = qs.filter(is_active=True)
    qs = qs.order_by("code")
    items = [
        ServiceTypeItem(
            id=st.id,
            code=st.code,
            name=st.name,
            description=st.description,
            requires_approval=st.requires_approval,
            is_active=st.is_active,
        )
        for st in qs
    ]
    return ServiceTypeListResponse(items=items)


def list_service_requests(
    status: Optional[str] = None,
    service_type_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    actor: Optional[User] = None,
) -> ServiceRequestListResponse:
    if actor:
        require_roles(actor, ["Administrator", "Tata Usaha", "Pimpinan"])

    qs = ServiceRequest.objects.select_related("service_type", "student").all()

    if status:
        qs = qs.filter(status=status)
    if service_type_id:
        qs = qs.filter(service_type_id=service_type_id)
    if search:
        search = search.strip()
        qs = qs.filter(Q(request_number__icontains=search) | Q(applicant_name__icontains=search))

    qs = qs.order_by("-created_at")

    paginator = Paginator(qs, page_size)
    p = paginator.get_page(page)

    items = [
        ServiceRequestItem(
            id=req.id,
            request_number=req.request_number,
            service_type_id=req.service_type_id,
            service_type_name=req.service_type.name,
            applicant_name=req.applicant_name,
            applicant_phone=req.applicant_phone,
            student_id=req.student_id,
            student_name=req.student.full_name if req.student else None,
            purpose=req.purpose,
            status=req.status,
            version=req.version,
            created_at=req.created_at,
        )
        for req in p.object_list
    ]

    return ServiceRequestListResponse(
        items=items,
        total=paginator.count,
        page=page,
        page_size=page_size,
    )


def get_service_request_detail(request_id: int, actor: User) -> ServiceRequestDetailResponse:
    require_roles(actor, ["Administrator", "Tata Usaha", "Pimpinan"])

    req = (
        ServiceRequest.objects.select_related("service_type", "student")
        .prefetch_related("documents", "events__actor")
        .filter(id=request_id)
        .first()
    )
    if not req:
        raise NotFoundError("Permohonan surat tidak ditemukan.")

    doc_items = [
        DocumentItem(
            id=d.id,
            request_id=d.request_id,
            storage_key=d.storage_key,
            original_filename=d.original_filename,
            mime_type=d.mime_type,
            file_size=d.file_size,
            created_at=d.created_at,
        )
        for d in req.documents.all()
    ]

    event_items = [
        ServiceEventItem(
            id=ev.id,
            action=ev.action,
            initial_status=ev.initial_status,
            final_status=ev.final_status,
            note=ev.note,
            actor_id=ev.actor_id,
            actor_name=ev.actor.full_name,
            created_at=ev.created_at,
        )
        for ev in req.events.all()
    ]

    return ServiceRequestDetailResponse(
        id=req.id,
        request_number=req.request_number,
        service_type_id=req.service_type_id,
        service_type_name=req.service_type.name,
        applicant_name=req.applicant_name,
        applicant_phone=req.applicant_phone,
        student_id=req.student_id,
        student_name=req.student.full_name if req.student else None,
        purpose=req.purpose,
        status=req.status,
        version=req.version,
        created_at=req.created_at,
        documents=doc_items,
        events=event_items,
    )


def list_archived_documents(
    search: Optional[str] = None,
    service_type_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
    actor: Optional[User] = None,
) -> DocumentListResponse:
    if actor:
        require_roles(actor, ["Administrator", "Tata Usaha", "Pimpinan"])

    qs = Document.objects.select_related("request").all()

    if service_type_id:
        qs = qs.filter(request__service_type_id=service_type_id)
    if search:
        search = search.strip()
        qs = qs.filter(Q(original_filename__icontains=search) | Q(request__request_number__icontains=search))

    qs = qs.order_by("-created_at")

    paginator = Paginator(qs, page_size)
    p = paginator.get_page(page)

    items = [
        DocumentItem(
            id=d.id,
            request_id=d.request_id,
            storage_key=d.storage_key,
            original_filename=d.original_filename,
            mime_type=d.mime_type,
            file_size=d.file_size,
            created_at=d.created_at,
        )
        for d in p.object_list
    ]

    return DocumentListResponse(
        items=items,
        total=paginator.count,
        page=page,
        page_size=page_size,
    )


def get_document_for_download(document_id: int, actor: User) -> Tuple[Document, Path]:
    require_roles(actor, ["Administrator", "Tata Usaha", "Pimpinan"])

    doc = Document.objects.filter(id=document_id).first()
    if not doc:
        raise NotFoundError("Dokumen arsip tidak ditemukan.")

    file_path = Path(settings.PRIVATE_MEDIA_ROOT) / doc.storage_key
    if not file_path.exists():
        raise NotFoundError("Berkas fisik tidak ditemukan pada media privat server.")

    return doc, file_path
