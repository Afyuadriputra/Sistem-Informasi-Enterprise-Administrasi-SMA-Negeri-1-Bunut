from datetime import date
from typing import Optional

from django.core.cache import cache
from django.core.paginator import Paginator
from django.utils import timezone

from apps.accounts.models import ActivityLog, User
from apps.administration.models import ServiceRequest, ServiceRequestStatusEnum
from apps.attendance.models import Attendance, AttendanceStatusEnum
from apps.core.security import require_roles
from apps.master_data.models import ClassAssignment, Student
from apps.reports.schemas import (
    AttendanceSummary,
    AuditLogItem,
    AuditLogListResponse,
    DashboardMetrics,
    DashboardMetricsResponse,
)
from apps.student_affairs.models import CaseStatusEnum, StudentCase


def get_dashboard_metrics(
    actor: User,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    use_cache: bool = True,
) -> DashboardMetricsResponse:
    # Determine primary role
    user_roles = {r.name for r in actor.roles.all()}
    if "Administrator" in user_roles:
        role_scope = "Administrator"
    elif "Pimpinan" in user_roles:
        role_scope = "Pimpinan"
    elif "Kesiswaan" in user_roles:
        role_scope = "Kesiswaan"
    elif "Tata Usaha" in user_roles:
        role_scope = "Tata Usaha"
    elif "Guru" in user_roles or "Guru Mapel" in user_roles or "Wali Kelas" in user_roles:
        role_scope = "Guru"
    else:
        role_scope = list(user_roles)[0] if user_roles else "Umum"

    clean_scope = role_scope.replace(" ", "_").lower()
    cache_key = f"dashboard:metrics:{actor.id}:{clean_scope}:{start_date}:{end_date}"
    if use_cache:
        cached_data = cache.get(cache_key)
        if cached_data:
            return DashboardMetricsResponse(**cached_data)

    today = timezone.localdate()
    now = timezone.now()

    def _get_att_date_filter():
        if start_date and end_date:
            return {"date__gte": start_date, "date__lte": end_date}
        elif start_date:
            return {"date__gte": start_date}
        elif end_date:
            return {"date__lte": end_date}
        return {"date": today}

    att_date_filter = _get_att_date_filter()

    # Calculate metrics by role
    if role_scope in ("Administrator", "Pimpinan"):
        active_students = Student.objects.filter(status="AKTIF").count()
        pending_cases = StudentCase.objects.filter(status__in=[CaseStatusEnum.BARU, CaseStatusEnum.DIPROSES]).count()

        if role_scope == "Pimpinan":
            pending_requests = ServiceRequest.objects.filter(
                status=ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN
            ).count()
        else:
            pending_requests = ServiceRequest.objects.filter(
                status__in=[
                    ServiceRequestStatusEnum.DIAJUKAN,
                    ServiceRequestStatusEnum.DIPROSES,
                    ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
                ]
            ).count()

        att_today_qs = Attendance.objects.filter(**att_date_filter)
        recorded_today = att_today_qs.exists()
        att_rate = None
        if recorded_today:
            total_records = att_today_qs.count()
            present_records = att_today_qs.filter(status=AttendanceStatusEnum.HADIR).count()
            att_rate = round((present_records / total_records) * 100, 2) if total_records > 0 else 0.0

        metrics = DashboardMetrics(
            attendance_summary=AttendanceSummary(
                recorded_today=recorded_today,
                attendance_rate_pct=att_rate,
            ),
            pending_cases_count=pending_cases,
            pending_requests_count=pending_requests,
            active_students_count=active_students,
        )

    elif role_scope == "Kesiswaan":
        active_students = Student.objects.filter(status="AKTIF").count()
        pending_cases = StudentCase.objects.filter(status__in=[CaseStatusEnum.BARU, CaseStatusEnum.DIPROSES]).count()
        att_today_qs = Attendance.objects.filter(**att_date_filter)
        recorded_today = att_today_qs.exists()
        att_rate = None
        if recorded_today:
            total_records = att_today_qs.count()
            present_records = att_today_qs.filter(status=AttendanceStatusEnum.HADIR).count()
            att_rate = round((present_records / total_records) * 100, 2) if total_records > 0 else 0.0

        metrics = DashboardMetrics(
            attendance_summary=AttendanceSummary(
                recorded_today=recorded_today,
                attendance_rate_pct=att_rate,
            ),
            pending_cases_count=pending_cases,
            pending_requests_count=0,
            active_students_count=active_students,
        )

    elif role_scope == "Tata Usaha":
        active_students = Student.objects.filter(status="AKTIF").count()
        pending_requests = ServiceRequest.objects.filter(
            status__in=[
                ServiceRequestStatusEnum.DIAJUKAN,
                ServiceRequestStatusEnum.DIPROSES,
                ServiceRequestStatusEnum.MENUNGGU_PERSETUJUAN,
            ]
        ).count()

        metrics = DashboardMetrics(
            attendance_summary=None,
            pending_cases_count=0,
            pending_requests_count=pending_requests,
            active_students_count=active_students,
        )

    elif role_scope == "Guru":
        assigned_class_ids = list(
            ClassAssignment.objects.filter(employee__user=actor).values_list("school_class_id", flat=True)
        )
        active_students = (
            Student.objects.filter(
                enrollments__school_class_id__in=assigned_class_ids,
                enrollments__end_date__isnull=True,
                status="AKTIF",
            )
            .distinct()
            .count()
        )

        homeroom_class_ids = list(
            ClassAssignment.objects.filter(employee__user=actor, role__in=["WALI_KELAS", "Wali Kelas"]).values_list(
                "school_class_id", flat=True
            )
        )
        pending_cases = 0
        if homeroom_class_ids:
            pending_cases = (
                StudentCase.objects.filter(
                    student__enrollments__school_class_id__in=homeroom_class_ids,
                    student__enrollments__end_date__isnull=True,
                    status__in=[CaseStatusEnum.BARU, CaseStatusEnum.DIPROSES],
                )
                .distinct()
                .count()
            )

        att_today_qs = Attendance.objects.filter(school_class_id__in=assigned_class_ids, **att_date_filter)
        recorded_today = att_today_qs.exists()
        att_rate = None
        if recorded_today:
            total_records = att_today_qs.count()
            present_records = att_today_qs.filter(status=AttendanceStatusEnum.HADIR).count()
            att_rate = round((present_records / total_records) * 100, 2) if total_records > 0 else 0.0

        metrics = DashboardMetrics(
            attendance_summary=AttendanceSummary(
                recorded_today=recorded_today,
                attendance_rate_pct=att_rate,
            ),
            pending_cases_count=pending_cases,
            pending_requests_count=0,
            active_students_count=active_students,
        )

    else:
        metrics = DashboardMetrics(
            attendance_summary=None,
            pending_cases_count=0,
            pending_requests_count=0,
            active_students_count=Student.objects.filter(status="AKTIF").count(),
        )

    response_data = DashboardMetricsResponse(
        role_scope=role_scope,
        generated_at=now,
        metrics=metrics,
    )

    if use_cache:
        # Cache for 5 minutes
        cache.set(cache_key, response_data.model_dump(mode="json"), timeout=300)

    return response_data


def list_audit_logs(
    actor: User,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    page_size: int = 20,
) -> AuditLogListResponse:
    require_roles(actor, ["Administrator"])

    qs = ActivityLog.objects.select_related("actor").all()

    if action:
        qs = qs.filter(action=action)
    if user_id:
        qs = qs.filter(actor_id=user_id)
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)

    qs = qs.order_by("-created_at")

    paginator = Paginator(qs, page_size)
    p = paginator.get_page(page)

    items = [
        AuditLogItem(
            id=log.id,
            actor_username=log.actor.username if log.actor else None,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            request_id=log.request_id,
            created_at=log.created_at,
        )
        for log in p.object_list
    ]

    return AuditLogListResponse(
        items=items,
        total=paginator.count,
        page=page,
        page_size=page_size,
    )
