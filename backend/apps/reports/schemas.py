from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AttendanceSummary(BaseModel):
    recorded_today: Optional[bool] = None
    attendance_rate_pct: Optional[float] = None


class DashboardMetrics(BaseModel):
    attendance_summary: Optional[AttendanceSummary] = None
    pending_cases_count: Optional[int] = None
    pending_requests_count: Optional[int] = None
    active_students_count: Optional[int] = None


class DashboardMetricsResponse(BaseModel):
    role_scope: str
    generated_at: datetime
    metrics: DashboardMetrics


class AuditLogItem(BaseModel):
    id: int
    actor_username: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    request_id: Optional[str] = None
    created_at: datetime


class AuditLogListResponse(BaseModel):
    items: List[AuditLogItem]
    total: int
    page: int
    page_size: int
