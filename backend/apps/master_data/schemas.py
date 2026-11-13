from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


# Academic Year Schemas
class AcademicYearItem(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    is_active: bool


class AcademicYearListResponse(BaseModel):
    items: List[AcademicYearItem]
    total: int
    page: int
    page_size: int


class AcademicYearCreateRequest(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_active: bool = False


class AcademicYearUpdateRequest(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


# School Class Schemas
class ClassItem(BaseModel):
    id: int
    academic_year_id: int
    academic_year_name: Optional[str] = None
    name: str
    level: int


class ClassListResponse(BaseModel):
    items: List[ClassItem]
    total: int
    page: int
    page_size: int


class ClassCreateRequest(BaseModel):
    academic_year_id: int
    name: str
    level: int


class ClassUpdateRequest(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None


# Employee Schemas
class EmployeeItem(BaseModel):
    id: int
    user_id: Optional[int] = None
    nip: Optional[str] = None
    name: str
    phone: Optional[str] = None
    status: str
    created_at: datetime


class EmployeeListResponse(BaseModel):
    items: List[EmployeeItem]
    total: int
    page: int
    page_size: int


class EmployeeCreateRequest(BaseModel):
    nip: Optional[str] = None
    name: str
    phone: Optional[str] = None
    status: str = "AKTIF"


class EmployeeUpdateRequest(BaseModel):
    nip: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None


# Student Schemas
class StudentItem(BaseModel):
    id: int
    student_number: str
    name: str
    gender: str
    status: str


class StudentListResponse(BaseModel):
    items: List[StudentItem]
    total: int
    page: int
    page_size: int


class StudentCreateRequest(BaseModel):
    student_number: str
    name: str
    gender: str
    status: str = "AKTIF"


class StudentUpdateRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    status: Optional[str] = None


# Enrollment Schemas
class EnrollmentItem(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    student_number: Optional[str] = None
    class_id: int
    class_name: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None


class EnrollmentListResponse(BaseModel):
    items: List[EnrollmentItem]
    total: int
    page: int
    page_size: int


class EnrollmentCreateRequest(BaseModel):
    student_id: int
    class_id: int
    start_date: date


class EnrollmentUpdateRequest(BaseModel):
    end_date: Optional[date] = None


# Class Assignment Schemas
class ClassAssignmentItem(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    employee_nip: Optional[str] = None
    class_id: int
    class_name: Optional[str] = None
    role: str
    start_date: date
    end_date: Optional[date] = None


class ClassAssignmentListResponse(BaseModel):
    items: List[ClassAssignmentItem]
    total: int
    page: int
    page_size: int


class ClassAssignmentCreateRequest(BaseModel):
    employee_id: int
    class_id: int
    role: str = "GURU_MAPEL"
    start_date: date


class ClassAssignmentUpdateRequest(BaseModel):
    end_date: Optional[date] = None
