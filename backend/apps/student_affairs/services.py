from typing import Optional

from django.db import transaction

from apps.accounts.models import ActivityLog, User
from apps.core.exceptions import (
    BusinessValidationError,
    ConcurrencyConflictError,
    NotFoundError,
)
from apps.core.security import require_roles
from apps.master_data.models import Student
from apps.reports.services import invalidate_dashboard_cache
from apps.student_affairs.models import (
    CaseActionEnum,
    CaseEvent,
    CaseStatusEnum,
    StudentCase,
)
from apps.student_affairs.schemas import (
    CaseTransitionRequest,
    CaseTransitionResponse,
    StudentCaseCreateRequest,
)


@transaction.atomic
def create_case(data: StudentCaseCreateRequest, actor: User, request_id: Optional[str] = None) -> StudentCase:
    require_roles(actor, ["Kesiswaan", "Wali Kelas"])
    student = Student.objects.filter(id=data.student_id).first()
    if not student:
        raise NotFoundError("Data siswa tidak ditemukan.")

    case = StudentCase.objects.create(
        student=student,
        title=data.title,
        summary=data.summary,
        status=CaseStatusEnum.BARU,
        assigned_to=actor.employee_profile if hasattr(actor, "employee_profile") else None,
        version=1,
    )

    CaseEvent.objects.create(
        case=case,
        action="BUAT_KASUS",
        initial_status=CaseStatusEnum.BARU,
        final_status=CaseStatusEnum.BARU,
        note=data.summary,
        actor=actor,
    )

    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_STUDENT_CASE",
        resource_type="student_affairs",
        resource_id=str(case.id),
        request_id=request_id,
        metadata=f'{{"case_title": "{case.title}"}}',
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return case


@transaction.atomic
def transition_case(
    case_id: int, data: CaseTransitionRequest, actor: User, request_id: Optional[str] = None
) -> CaseTransitionResponse:
    require_roles(actor, ["Kesiswaan"])
    case = StudentCase.objects.select_for_update().filter(id=case_id).first()
    if not case:
        raise NotFoundError("Kasus kesiswaan tidak ditemukan.")

    if case.status in (CaseStatusEnum.SELESAI, CaseStatusEnum.DIBATALKAN):
        raise BusinessValidationError(
            f"Kasus telah berada pada status akhir '{case.status}' dan tidak dapat diubah lagi."
        )

    # Optimistic locking check
    if case.version != data.expected_version:
        raise ConcurrencyConflictError(
            message="Data kasus telah diubah oleh pengguna lain. Silakan muat ulang halaman.",
            details=[{"current_version": case.version, "provided_version": data.expected_version}],
        )

    initial_status = case.status
    if data.action == CaseActionEnum.MULAI_PENANGANAN:
        if case.status != CaseStatusEnum.BARU:
            raise BusinessValidationError("Aksi MULAI_PENANGANAN hanya dapat dilakukan pada kasus berstatus BARU.")
        final_status = CaseStatusEnum.DIPROSES

    elif data.action == CaseActionEnum.CATAT_TINDAKAN:
        if case.status not in (CaseStatusEnum.BARU, CaseStatusEnum.DIPROSES):
            raise BusinessValidationError("Aksi CATAT_TINDAKAN hanya dapat dilakukan pada kasus yang aktif.")
        if not data.note or not data.note.strip():
            raise BusinessValidationError("Catatan tindakan konseling wajib diisi.")
        final_status = case.status  # status unchanged

    elif data.action == CaseActionEnum.SELESAIKAN:
        if case.status != CaseStatusEnum.DIPROSES:
            raise BusinessValidationError("Kasus harus berstatus DIPROSES sebelum dapat diselesaikan.")
        final_status = CaseStatusEnum.SELESAI

    elif data.action == CaseActionEnum.BATALKAN:
        if case.status not in (CaseStatusEnum.BARU, CaseStatusEnum.DIPROSES):
            raise BusinessValidationError("Kasus tidak dapat dibatalkan pada status saat ini.")
        if not data.note or not data.note.strip():
            raise BusinessValidationError("Alasan pembatalan kasus wajib diisi.")
        final_status = CaseStatusEnum.DIBATALKAN

    else:
        raise BusinessValidationError(f"Aksi '{data.action}' tidak valid.")

    case.status = final_status
    case.version += 1
    case.save()

    CaseEvent.objects.create(
        case=case,
        action=data.action,
        initial_status=initial_status,
        final_status=final_status,
        note=data.note,
        actor=actor,
    )

    ActivityLog.objects.create(
        actor=actor,
        action="TRANSITION_STUDENT_CASE",
        resource_type="student_affairs",
        resource_id=str(case.id),
        request_id=request_id,
        metadata=f'{{"action": "{data.action}", "version": {case.version}}}',
    )
    transaction.on_commit(invalidate_dashboard_cache)

    return CaseTransitionResponse(
        id=case.id,
        status=case.status,
        version=case.version,
        message="Status kasus berhasil diperbarui.",
    )
