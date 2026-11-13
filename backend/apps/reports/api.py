from datetime import date
from typing import Optional

from django.http import HttpResponse
from ninja import Router

from apps.core.security import jwt_auth
from apps.reports import selectors, services
from apps.reports.schemas import AuditLogListResponse, DashboardMetricsResponse

reports_router = Router(tags=["Reports"])
audit_router = Router(tags=["Audit"])


@reports_router.get(
    "/dashboard",
    auth=jwt_auth,
    response=DashboardMetricsResponse,
    operation_id="getDashboardMetrics",
)
def get_dashboard_metrics(
    request,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    return selectors.get_dashboard_metrics(actor=request.user)


@reports_router.get(
    "/attendance.xlsx",
    auth=jwt_auth,
    operation_id="exportAttendanceExcel",
)
def export_attendance_excel(
    request,
    start_date: date,
    end_date: date,
    class_id: Optional[int] = None,
):
    excel_stream = services.generate_attendance_excel(
        start_date=start_date,
        end_date=end_date,
        actor=request.user,
        class_id=class_id,
    )
    filename = f"rekap_kehadiran_{start_date}_{end_date}.xlsx"
    response = HttpResponse(
        excel_stream.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@reports_router.get(
    "/administration.pdf",
    auth=jwt_auth,
    operation_id="exportAdministrationPdf",
)
def export_administration_pdf(
    request,
    start_date: date,
    end_date: date,
    service_type_id: Optional[int] = None,
):
    pdf_stream = services.generate_administration_pdf(
        start_date=start_date,
        end_date=end_date,
        actor=request.user,
        service_type_id=service_type_id,
    )
    filename = f"laporan_administrasi_{start_date}_{end_date}.pdf"
    response = HttpResponse(pdf_stream.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@audit_router.get(
    "",
    auth=jwt_auth,
    response=AuditLogListResponse,
    operation_id="listAuditLogs",
)
def list_audit_logs(
    request,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    page_size: int = 20,
):
    return selectors.list_audit_logs(
        actor=request.user,
        action=action,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )
