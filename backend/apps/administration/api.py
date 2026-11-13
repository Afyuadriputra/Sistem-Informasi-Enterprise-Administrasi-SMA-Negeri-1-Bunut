from typing import Optional

from django.http import FileResponse
from ninja import File, Router
from ninja.files import UploadedFile
from ninja.responses import Response

from apps.administration import selectors, services
from apps.administration.schemas import (
    DocumentItem,
    DocumentListResponse,
    ServiceRequestCreateRequest,
    ServiceRequestDetailResponse,
    ServiceRequestItem,
    ServiceRequestListResponse,
    ServiceTransitionRequest,
    ServiceTransitionResponse,
    ServiceTypeCreateRequest,
    ServiceTypeItem,
    ServiceTypeListResponse,
    ServiceTypeUpdateRequest,
)
from apps.core.security import jwt_auth, require_roles

router = Router(tags=["Administration"])
administration_router = router


@router.get("/service-types", auth=jwt_auth, response=ServiceTypeListResponse, operation_id="listServiceTypes")
def list_service_types(request):
    return selectors.list_service_types()


@router.post("/service-types", auth=jwt_auth, response={201: ServiceTypeItem}, operation_id="createServiceType")
def create_service_type(request, data: ServiceTypeCreateRequest):
    require_roles(request.user, ["Administrator"])
    st = services.create_service_type(data=data, actor=request.user)
    item = ServiceTypeItem(
        id=st.id,
        code=st.code,
        name=st.name,
        description=st.description,
        requires_approval=st.requires_approval,
        is_active=st.is_active,
    )
    return Response(item.model_dump(), status=201)


@router.patch("/service-types/{id}", auth=jwt_auth, response=ServiceTypeItem, operation_id="updateServiceType")
def update_service_type(request, id: int, data: ServiceTypeUpdateRequest):
    require_roles(request.user, ["Administrator"])
    st = services.update_service_type(type_id=id, data=data, actor=request.user)
    return ServiceTypeItem(
        id=st.id,
        code=st.code,
        name=st.name,
        description=st.description,
        requires_approval=st.requires_approval,
        is_active=st.is_active,
    )


@router.get("/requests", auth=jwt_auth, response=ServiceRequestListResponse, operation_id="listServiceRequests")
def list_service_requests(
    request,
    status: Optional[str] = None,
    service_type_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    return selectors.list_service_requests(
        status=status,
        service_type_id=service_type_id,
        search=search,
        page=page,
        page_size=page_size,
        actor=request.user,
    )


@router.post("/requests", auth=jwt_auth, response={201: ServiceRequestItem}, operation_id="createServiceRequest")
def create_service_request(request, data: ServiceRequestCreateRequest):
    require_roles(request.user, ["Tata Usaha"])
    request_id_header = getattr(request, "request_id", None)
    req = services.create_service_request(data=data, actor=request.user, request_id=request_id_header)
    item = ServiceRequestItem(
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
    return Response(item.model_dump(), status=201)


@router.get(
    "/requests/{id}",
    auth=jwt_auth,
    response=ServiceRequestDetailResponse,
    operation_id="getServiceRequestDetail",
)
def get_service_request_detail(request, id: int):
    return selectors.get_service_request_detail(request_id=id, actor=request.user)


@router.post(
    "/requests/{id}/transitions",
    auth=jwt_auth,
    response=ServiceTransitionResponse,
    operation_id="transitionServiceRequest",
)
def transition_service_request(request, id: int, data: ServiceTransitionRequest):
    request_id_header = getattr(request, "request_id", None)
    return services.transition_service_request(
        request_id=id,
        data=data,
        actor=request.user,
        request_id_header=request_id_header,
    )


@router.post(
    "/requests/{id}/documents",
    auth=jwt_auth,
    response={201: DocumentItem},
    operation_id="uploadRequestDocument",
)
def upload_request_document(request, id: int, file: UploadedFile = File(...)):
    doc = services.upload_service_document(request_id=id, uploaded_file=file, actor=request.user)
    item = DocumentItem(
        id=doc.id,
        request_id=doc.request_id,
        storage_key=doc.storage_key,
        original_filename=doc.original_filename,
        mime_type=doc.mime_type,
        file_size=doc.file_size,
        created_at=doc.created_at,
    )
    return Response(item.model_dump(), status=201)


@router.get("/documents", auth=jwt_auth, response=DocumentListResponse, operation_id="listArchivedDocuments")
def list_archived_documents(
    request,
    search: Optional[str] = None,
    service_type_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
):
    return selectors.list_archived_documents(
        search=search,
        service_type_id=service_type_id,
        page=page,
        page_size=page_size,
        actor=request.user,
    )


@router.get("/documents/{id}/download", auth=jwt_auth, operation_id="downloadPrivateDocument")
def download_private_document(request, id: int):
    doc, file_path = selectors.get_document_for_download(document_id=id, actor=request.user)
    response = FileResponse(open(file_path, "rb"), content_type=doc.mime_type)
    response["Content-Disposition"] = f'attachment; filename="{doc.original_filename}"'
    return response
