from datetime import date
from typing import Optional

from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.db.models import Q
from simple_history.utils import bulk_create_with_history, bulk_update_with_history

from apps.accounts.models import ActivityLog, User
from apps.attendance.models import Attendance, AttendanceStatusEnum
from apps.attendance.schemas import AttendanceBulkRequest, AttendanceBulkResponse
from apps.core.exceptions import BusinessValidationError, ConcurrencyConflictError, NotFoundError, PermissionDeniedError
from apps.core.security import require_roles
from apps.master_data.models import ClassAssignment, Enrollment, SchoolClass
from apps.reports.services import invalidate_dashboard_cache


@transaction.atomic
def save_bulk_attendance(
    payload: AttendanceBulkRequest, actor: User, request_id: Optional[str] = None
) -> AttendanceBulkResponse:
    # 1. Date validation
    if payload.date > date.today():
        raise BusinessValidationError("Tanggal absensi tidak boleh melebihi tanggal berjalan.")

    # 2. Class validation
    school_class = SchoolClass.objects.filter(id=payload.class_id).first()
    if not school_class:
        raise NotFoundError("Kelas tidak ditemukan.")

    # 2b. Optimistic locking check for roster revision (CCR-20261114-01)
    current_roster_ver = Attendance.history.filter(school_class=school_class, date=payload.date).count()
    if payload.expected_roster_version is not None and payload.expected_roster_version != current_roster_ver:
        raise ConcurrencyConflictError(
            message="Data presensi kelas ini telah diperbarui oleh pengguna lain. Silakan muat ulang roster sebelum menyimpan.",
            details=[{"current_roster_version": current_roster_ver, "expected_roster_version": payload.expected_roster_version}],
        )

    # 3. Authorization validation: strictly assigned teacher/homeroom
    require_roles(actor, ["Guru", "Wali Kelas"])
    if not hasattr(actor, "employee_profile") or not actor.employee_profile:
        raise PermissionDeniedError("Akun Anda tidak terhubung dengan profil pegawai/guru.")

    has_assignment = (
        ClassAssignment.objects.filter(
            employee=actor.employee_profile,
            school_class=school_class,
            start_date__lte=payload.date,
        )
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=payload.date))
        .exists()
    )

    if not has_assignment:
        raise PermissionDeniedError("Anda tidak memiliki penugasan aktif di kelas ini pada tanggal tersebut.")

    # 4. Duplicate students check in payload
    student_ids = [item.student_id for item in payload.items]
    if len(student_ids) != len(set(student_ids)):
        raise BusinessValidationError("Terdapat duplikasi data siswa dalam satu batch absensi.")

    # 5. Enrolled students verification
    enrolled_ids = set(
        Enrollment.objects.filter(
            school_class=school_class,
            start_date__lte=payload.date,
        )
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=payload.date))
        .values_list("student_id", flat=True)
    )

    invalid_students = [sid for sid in student_ids if sid not in enrolled_ids]
    if invalid_students:
        details = [
            {
                "field": f"student_id_{sid}",
                "message": f"Siswa ID {sid} tidak terdaftar aktif di kelas ini pada tanggal {payload.date}.",
            }
            for sid in invalid_students
        ]
        raise BusinessValidationError(
            "Data baris tidak valid atau terdapat siswa tidak terdaftar di kelas ini.",
            details=details,
        )

    # Validate statuses
    valid_statuses = set(AttendanceStatusEnum.values)
    for item in payload.items:
        if item.status not in valid_statuses:
            raise BusinessValidationError(f"Status absensi '{item.status}' tidak valid.")

    # 6. Bulk persistence with history
    existing_records = {
        a.student_id: a for a in Attendance.objects.filter(school_class=school_class, date=payload.date)
    }

    to_create = []
    to_update = []

    for item in payload.items:
        if item.student_id in existing_records:
            rec = existing_records[item.student_id]
            rec.status = item.status
            rec.note = item.note or ""
            rec.recorded_by = actor
            rec._change_reason = f"Bulk update presensi oleh {actor.username}"
            to_update.append(rec)
        else:
            new_rec = Attendance(
                student_id=item.student_id,
                school_class=school_class,
                date=payload.date,
                status=item.status,
                note=item.note or "",
                recorded_by=actor,
            )
            new_rec._change_reason = f"Bulk create presensi oleh {actor.username}"
            to_create.append(new_rec)

    try:
        if to_create:
            bulk_create_with_history(to_create, Attendance, default_user=actor)

        if to_update:
            bulk_update_with_history(to_update, Attendance, ["status", "note", "recorded_by"], default_user=actor)
    except IntegrityError:
        raise ConcurrencyConflictError(
            message="Terjadi benturan data presensi secara serentak oleh pengguna lain. Silakan muat ulang roster sebelum menyimpan.",
            details=[{"conflict": "Unique constraint violation on concurrent submission"}],
        )

    # Invalidate cache after commit
    def invalidate_cache():
        cache.delete(f"attendance:recap:{school_class.id}")
        cache.delete("dashboard:attendance_metrics")

    transaction.on_commit(invalidate_cache)
    transaction.on_commit(invalidate_dashboard_cache)

    ActivityLog.objects.create(
        actor=actor,
        action="ATTENDANCE_BULK_SAVE",
        resource_type="attendance",
        resource_id=str(school_class.id),
        request_id=request_id,
        metadata=f'{{"date": "{payload.date}", "count": {len(payload.items)}}}',
    )

    return AttendanceBulkResponse(
        class_id=payload.class_id,
        date=payload.date,
        saved_count=len(payload.items),
        message="Kehadiran berhasil disimpan.",
    )
