from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class AttendanceRosterItem(BaseModel):
    student_id: int
    student_name: str
    student_number: str
    current_status: Optional[str] = None
    current_note: Optional[str] = None


class AttendanceRosterResponse(BaseModel):
    class_id: int
    class_name: str
    date: date
    students: List[AttendanceRosterItem]
    roster_version: int = 0


class AttendanceBulkItem(BaseModel):
    student_id: int
    status: str
    note: str = ""


class AttendanceBulkRequest(BaseModel):
    class_id: int
    date: date
    items: List[AttendanceBulkItem]
    expected_roster_version: Optional[int] = None


class AttendanceBulkResponse(BaseModel):
    class_id: int
    date: date
    saved_count: int
    message: str


class AttendanceSummaryItem(BaseModel):
    total_students: int
    hadir_pct: float
    sakit_count: int
    izin_count: int
    alpa_count: int


class StudentRecapItem(BaseModel):
    student_id: int
    student_name: str
    student_number: str
    hadir: int
    sakit: int
    izin: int
    alpa: int


class AttendanceRecapResponse(BaseModel):
    summary: AttendanceSummaryItem
    student_recaps: List[StudentRecapItem]
