from datetime import date
from typing import Optional

from django.http import HttpRequest
from ninja import Query, Router

from apps.attendance.schemas import (
    AttendanceBulkRequest,
    AttendanceBulkResponse,
    AttendanceRecapResponse,
    AttendanceRosterResponse,
)
from apps.attendance.selectors import get_attendance_recap, get_attendance_roster
from apps.attendance.services import save_bulk_attendance
from apps.core.security import jwt_auth

attendance_router = Router(tags=["Attendance"], auth=jwt_auth)


@attendance_router.get(
    "/roster",
    response={200: AttendanceRosterResponse},
    operation_id="getAttendanceRoster",
)
def get_roster(
    request: HttpRequest,
    class_id: int = Query(...),
    date: date = Query(...),
):
    return get_attendance_roster(class_id=class_id, target_date=date, actor=request.user)


@attendance_router.post(
    "/bulk",
    response={200: AttendanceBulkResponse},
    operation_id="saveAttendanceBulk",
)
def post_bulk(
    request: HttpRequest,
    payload: AttendanceBulkRequest,
):
    req_id = getattr(request, "request_id", None)
    return save_bulk_attendance(payload=payload, actor=request.user, request_id=req_id)


@attendance_router.get(
    "",
    response={200: AttendanceRecapResponse},
    operation_id="getAttendanceRecap",
)
def get_recap(
    request: HttpRequest,
    class_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    return get_attendance_recap(
        class_id=class_id,
        start_date=start_date,
        end_date=end_date,
        actor=request.user,
    )
