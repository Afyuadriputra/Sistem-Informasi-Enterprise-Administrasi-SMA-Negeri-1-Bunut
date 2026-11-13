from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ServiceTypeItem(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    requires_approval: bool
    is_active: bool


class ServiceTypeListResponse(BaseModel):
    items: List[ServiceTypeItem]


class ServiceTypeCreateRequest(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    requires_approval: bool = True
    is_active: bool = True


class ServiceTypeUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    requires_approval: Optional[bool] = None
    is_active: Optional[bool] = None


class DocumentItem(BaseModel):
    id: int
    request_id: int
    storage_key: str
    original_filename: str
    mime_type: str
    file_size: int
    created_at: datetime


class DocumentListResponse(BaseModel):
    items: List[DocumentItem]
    total: int
    page: int
    page_size: int


class ServiceEventItem(BaseModel):
    id: int
    action: str
    initial_status: str
    final_status: str
    note: Optional[str] = None
    actor_id: int
    actor_name: str
    created_at: datetime


class ServiceRequestItem(BaseModel):
    id: int
    request_number: str
    service_type_id: int
    service_type_name: str
    applicant_name: str
    applicant_phone: Optional[str] = None
    student_id: Optional[int] = None
    student_name: Optional[str] = None
    purpose: str
    status: str
    version: int
    created_at: datetime


class ServiceRequestDetailResponse(BaseModel):
    id: int
    request_number: str
    service_type_id: int
    service_type_name: str
    applicant_name: str
    applicant_phone: Optional[str] = None
    student_id: Optional[int] = None
    student_name: Optional[str] = None
    purpose: str
    status: str
    version: int
    created_at: datetime
    documents: List[DocumentItem]
    events: List[ServiceEventItem]


class ServiceRequestCreateRequest(BaseModel):
    service_type_id: int
    applicant_name: str
    applicant_phone: Optional[str] = None
    student_id: Optional[int] = None
    purpose: str


class ServiceTransitionRequest(BaseModel):
    action: str
    note: Optional[str] = None
    expected_version: int


class ServiceTransitionResponse(BaseModel):
    id: int
    status: str
    version: int
    message: str


class ServiceRequestListResponse(BaseModel):
    items: List[ServiceRequestItem]
    total: int
    page: int
    page_size: int
