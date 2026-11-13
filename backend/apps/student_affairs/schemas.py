from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CaseEventItem(BaseModel):
    id: int
    action: str
    initial_status: str
    final_status: str
    note: str
    actor_id: int
    actor_name: str
    created_at: datetime


class StudentCaseItem(BaseModel):
    id: int
    student_id: int
    student_name: str
    student_number: str
    class_name: Optional[str] = None
    title: str
    summary: str
    status: str
    assigned_to_id: Optional[int] = None
    assigned_to_name: Optional[str] = None
    version: int
    created_at: datetime


class StudentCaseDetailResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    student_number: str
    class_name: Optional[str] = None
    title: str
    summary: str
    status: str
    assigned_to_id: Optional[int] = None
    assigned_to_name: Optional[str] = None
    version: int
    created_at: datetime
    events: List[CaseEventItem]


class StudentCaseCreateRequest(BaseModel):
    student_id: int
    title: str
    summary: str
    assigned_to_id: Optional[int] = None


class CaseTransitionRequest(BaseModel):
    action: str
    note: str
    expected_version: int


class CaseTransitionResponse(BaseModel):
    id: int
    status: str
    version: int
    message: str


class StudentCaseListResponse(BaseModel):
    items: List[StudentCaseItem]
    total: int
    page: int
    page_size: int
