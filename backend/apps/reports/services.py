import io
from datetime import date
from typing import Optional

import openpyxl
from django.core.cache import cache
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.accounts.models import ActivityLog, User
from apps.administration.models import ServiceRequest
from apps.attendance.models import Attendance
from apps.core.exceptions import PermissionDeniedError
from apps.core.security import require_roles
from apps.master_data.models import ClassAssignment


def invalidate_dashboard_cache():
    """Invalidates cached dashboard metrics across users"""
    try:
        cache.clear()
    except Exception:
        pass


def sanitize_cell_value(val):
    """Sanitize cell value to prevent formula injection (CWE-1236)."""
    if isinstance(val, str) and val.startswith(("=", "+", "-", "@")):
        return f"'{val}"
    return val


def generate_attendance_excel(
    start_date: date,
    end_date: date,
    actor: User,
    class_id: Optional[int] = None,
) -> io.BytesIO:
    # 1. Role validation (Guru, Wali Kelas, Kesiswaan, Pimpinan)
    user_roles = {r.name for r in actor.roles.all()}
    allowed_roles = {"Guru", "Guru Mapel", "Wali Kelas", "Kesiswaan", "Pimpinan"}
    if not user_roles.intersection(allowed_roles):
        raise PermissionDeniedError("Peran Anda tidak memiliki wewenang ekspor kehadiran.")

    is_privileged = bool(user_roles.intersection({"Pimpinan", "Kesiswaan"}))

    qs = Attendance.objects.select_related("student", "school_class").filter(date__gte=start_date, date__lte=end_date)

    if not is_privileged:
        # Teacher must be assigned to the class
        assigned_class_ids = list(
            ClassAssignment.objects.filter(employee__user=actor).values_list("school_class_id", flat=True)
        )
        if class_id:
            if class_id not in assigned_class_ids:
                raise PermissionDeniedError("Anda tidak berwenang mengakses data kehadiran kelas ini.")
            qs = qs.filter(school_class_id=class_id)
        else:
            qs = qs.filter(school_class_id__in=assigned_class_ids)
    else:
        if class_id:
            qs = qs.filter(school_class_id=class_id)

    qs = qs.order_by("date", "school_class__name", "student__student_number")

    # 2. Build openpyxl workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rekap Kehadiran"

    # Header styling (institutional navy #173B63)
    header_fill = PatternFill(start_color="173B63", end_color="173B63", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC"),
    )

    # Title rows
    ws.merge_cells("A1:G1")
    title_cell = ws["A1"]
    title_cell.value = "REKAPITULASI KEHADIRAN SISWA - SMA NEGERI 1 BUNUT"
    title_cell.font = Font(name="Arial", size=14, bold=True, color="173B63")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A2:G2")
    sub_cell = ws["A2"]
    sub_cell.value = f"Periode: {start_date.strftime('%d/%m/%Y')} s/d {end_date.strftime('%d/%m/%Y')}"
    sub_cell.font = Font(name="Arial", size=10, italic=True)
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws.append([])  # Blank row

    headers = ["No", "Tanggal", "Kelas", "NISN/NIS", "Nama Siswa", "Status", "Catatan"]
    ws.append(headers)

    header_row = ws.max_row
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=header_row, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    # Data rows with formula injection sanitization
    row_num = 1
    for att in qs:
        raw_row = [
            row_num,
            att.date.strftime("%d/%m/%Y"),
            att.school_class.name,
            att.student.student_number,
            att.student.full_name,
            att.status,
            att.note or "-",
        ]
        ws.append([sanitize_cell_value(val) for val in raw_row])
        current_row = ws.max_row
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=current_row, column=col_idx)
            cell.border = thin_border
            if col_idx in (1, 2, 3, 6):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center")
        row_num += 1

    # Adjust column widths
    column_widths = [6, 14, 12, 16, 32, 14, 30]
    for i, width in enumerate(column_widths, start=1):
        col_letter = openpyxl.utils.get_column_letter(i)
        ws.column_dimensions[col_letter].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    ActivityLog.objects.create(
        actor=actor,
        action="EXPORT_ATTENDANCE_EXCEL",
        resource_type="reports",
        metadata=f'{{"start_date": "{start_date}", "end_date": "{end_date}", "class_id": {class_id}}}',
    )

    return output


def generate_administration_pdf(
    start_date: date,
    end_date: date,
    actor: User,
    service_type_id: Optional[int] = None,
) -> io.BytesIO:
    require_roles(actor, ["Tata Usaha", "Pimpinan"])

    qs = ServiceRequest.objects.select_related("service_type", "student").filter(
        created_at__date__gte=start_date, created_at__date__lte=end_date
    )

    if service_type_id:
        qs = qs.filter(service_type_id=service_type_id)

    qs = qs.order_by("-created_at")

    output = io.BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Title & subtitle
    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=colors.HexColor("#173B63"),
        alignment=1,  # Center
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#4B5563"),
        alignment=1,  # Center
        spaceAfter=14,
    )

    elements.append(Paragraph("PEMERINTAH KABUPATEN PELALAWAN", subtitle_style))
    elements.append(Paragraph("LAPORAN ADMINISTRASI PERSURATAN SISWA - SMA NEGERI 1 BUNUT", title_style))
    elements.append(
        Paragraph(
            f"Periode Pelaporan: {start_date.strftime('%d/%m/%Y')} s/d {end_date.strftime('%d/%m/%Y')}",
            subtitle_style,
        )
    )
    elements.append(Spacer(1, 10))

    # Table data
    table_headers = ["No", "Nomor Surat", "Jenis Layanan", "Pemohon", "Siswa", "Status", "Tanggal Buat"]
    table_data = [table_headers]

    idx = 1
    for r in qs:
        student_display = r.student.full_name if r.student else "-"
        table_data.append(
            [
                str(idx),
                r.request_number,
                r.service_type.name,
                r.applicant_name,
                student_display,
                r.status,
                r.created_at.strftime("%d/%m/%Y"),
            ]
        )
        idx += 1

    if len(table_data) == 1:
        table_data.append(["-", "Tidak ada data permohonan pada periode ini.", "", "", "", "", ""])

    t = Table(table_data, colWidths=[30, 130, 140, 120, 120, 90, 80])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173B63")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (2, 1), (4, -1), "LEFT"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
            ]
        )
    )
    elements.append(t)

    doc.build(elements)
    output.seek(0)

    ActivityLog.objects.create(
        actor=actor,
        action="EXPORT_ADMINISTRATION_PDF",
        resource_type="reports",
        metadata=f'{{"start_date": "{start_date}", "end_date": "{end_date}", "service_type_id": {service_type_id}}}',
    )

    return output
