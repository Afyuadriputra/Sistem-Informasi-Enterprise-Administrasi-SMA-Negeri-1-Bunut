from datetime import date
from typing import Optional

from django.db.models import Count, Q

from apps.accounts.models import User
from apps.attendance.models import Attendance, AttendanceStatusEnum
from apps.attendance.schemas import (
    AttendanceRecapResponse,
    AttendanceRosterItem,
    AttendanceRosterResponse,
    AttendanceSummaryItem,
    StudentRecapItem,
)
from apps.core.exceptions import NotFoundError, PermissionDeniedError
from apps.core.security import check_roles
from apps.master_data.models import ClassAssignment, Enrollment, SchoolClass


def get_attendance_roster(class_id: int, target_date: date, actor: User) -> AttendanceRosterResponse:
    school_class = SchoolClass.objects.filter(id=class_id).first()
    if not school_class:
        raise NotFoundError("Kelas tidak ditemukan.")

    # Authorization
    if not check_roles(actor, ["Administrator"]):
        if not hasattr(actor, "employee_profile") or not actor.employee_profile:
            raise PermissionDeniedError("Akun Anda tidak terhubung dengan profil pegawai/guru.")

        has_assignment = (
            ClassAssignment.objects.filter(
                employee=actor.employee_profile,
                school_class=school_class,
                start_date__lte=target_date,
            )
            .filter(Q(end_date__isnull=True) | Q(end_date__gte=target_date))
            .exists()
        )

        if not has_assignment:
            raise PermissionDeniedError("Anda tidak memiliki penugasan aktif di kelas ini pada tanggal tersebut.")

    # Fetch enrolled students
    enrollments = (
        Enrollment.objects.select_related("student")
        .filter(
            school_class=school_class,
            start_date__lte=target_date,
        )
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=target_date))
        .order_by("student__name")
    )

    # Fetch existing attendance on target_date
    attendances = {a.student_id: a for a in Attendance.objects.filter(school_class=school_class, date=target_date)}

    students = []
    for enr in enrollments:
        std = enr.student
        att = attendances.get(std.id)
        students.append(
            AttendanceRosterItem(
                student_id=std.id,
                student_name=std.name,
                student_number=std.student_number,
                current_status=att.status if att else None,
                current_note=att.note if att else None,
            )
        )

    roster_ver = Attendance.history.filter(school_class=school_class, date=target_date).count()

    return AttendanceRosterResponse(
        class_id=school_class.id,
        class_name=school_class.name,
        date=target_date,
        students=students,
        roster_version=roster_ver,
    )


def get_attendance_recap(
    class_id: Optional[int],
    start_date: Optional[date],
    end_date: Optional[date],
    actor: User,
) -> AttendanceRecapResponse:
    qs = Attendance.objects.select_related("student", "school_class")

    # Object-level permission scoping
    if not check_roles(actor, ["Administrator", "Pimpinan", "Kesiswaan"]):
        if not hasattr(actor, "employee_profile") or not actor.employee_profile:
            raise PermissionDeniedError("Akun Anda tidak terhubung dengan profil pegawai/guru.")

        assigned_class_ids = list(
            ClassAssignment.objects.filter(employee=actor.employee_profile, end_date__isnull=True).values_list(
                "school_class_id", flat=True
            )
        )

        if class_id:
            if class_id not in assigned_class_ids:
                raise PermissionDeniedError("Anda tidak memiliki akses rekapitulasi kelas ini.")
            qs = qs.filter(school_class_id=class_id)
        else:
            qs = qs.filter(school_class_id__in=assigned_class_ids)
    else:
        if class_id:
            qs = qs.filter(school_class_id=class_id)

    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)

    total_records = qs.count()
    sakit_count = qs.filter(status=AttendanceStatusEnum.SAKIT).count()
    izin_count = qs.filter(status=AttendanceStatusEnum.IZIN).count()
    alpa_count = qs.filter(status=AttendanceStatusEnum.ALPA).count()
    hadir_count = qs.filter(status=AttendanceStatusEnum.HADIR).count()

    hadir_pct = round((hadir_count / total_records * 100), 2) if total_records > 0 else 100.0

    # Student-level breakdowns
    student_stats = (
        qs.values("student_id", "student__name", "student__student_number")
        .annotate(
            hadir=Count("id", filter=Q(status=AttendanceStatusEnum.HADIR)),
            sakit=Count("id", filter=Q(status=AttendanceStatusEnum.SAKIT)),
            izin=Count("id", filter=Q(status=AttendanceStatusEnum.IZIN)),
            alpa=Count("id", filter=Q(status=AttendanceStatusEnum.ALPA)),
        )
        .order_by("student__name")
    )

    student_recaps = [
        StudentRecapItem(
            student_id=s["student_id"],
            student_name=s["student__name"],
            student_number=s["student__student_number"],
            hadir=s["hadir"],
            sakit=s["sakit"],
            izin=s["izin"],
            alpa=s["alpa"],
        )
        for s in student_stats
    ]

    total_students = len(student_recaps)

    summary = AttendanceSummaryItem(
        total_students=total_students,
        hadir_pct=hadir_pct,
        sakit_count=sakit_count,
        izin_count=izin_count,
        alpa_count=alpa_count,
    )

    return AttendanceRecapResponse(summary=summary, student_recaps=student_recaps)
