from typing import Optional

from django.db.models import Prefetch, Q

from apps.accounts.models import User
from apps.core.exceptions import NotFoundError, PermissionDeniedError
from apps.core.pagination import paginate_queryset
from apps.core.security import check_roles, require_roles
from apps.master_data.models import ClassAssignment, Enrollment
from apps.student_affairs.models import CaseActionEnum, StudentCase
from apps.student_affairs.schemas import (
    CaseEventItem,
    StudentCaseDetailResponse,
    StudentCaseItem,
    StudentCaseListResponse,
)


def _get_accessible_student_ids(actor: User) -> Optional[set]:
    """Returns None if actor can access all students (Kesiswaan),
    or set of student_ids if limited to homeroom class (Wali Kelas).
    Administrator and other roles are denied per RBAC_MATRIX.md Separation of Duties.
    """
    if check_roles(actor, ["Kesiswaan"]):
        return None

    if check_roles(actor, ["Wali Kelas"]):
        if not hasattr(actor, "employee_profile") or not actor.employee_profile:
            return set()

        homeroom_classes = ClassAssignment.objects.filter(
            employee=actor.employee_profile,
            role="WALI_KELAS",
            end_date__isnull=True,
        ).values_list("school_class_id", flat=True)

        student_ids = set(
            Enrollment.objects.filter(
                school_class_id__in=homeroom_classes,
                end_date__isnull=True,
            ).values_list("student_id", flat=True)
        )
        return student_ids

    raise PermissionDeniedError("Anda tidak memiliki akses ke modul kasus kesiswaan.")


def list_cases(
    status: Optional[str] = None,
    student_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    actor: Optional[User] = None,
) -> StudentCaseListResponse:
    if actor:
        require_roles(actor, ["Kesiswaan", "Wali Kelas"])

    active_enr_prefetch = Prefetch(
        "student__enrollments",
        queryset=Enrollment.objects.filter(end_date__isnull=True).select_related("school_class"),
        to_attr="active_enrollments_list",
    )
    qs = (
        StudentCase.objects.select_related("student", "assigned_to")
        .prefetch_related(active_enr_prefetch)
        .order_by("-created_at")
    )

    if actor:
        allowed_students = _get_accessible_student_ids(actor)
        if allowed_students is not None:
            qs = qs.filter(student_id__in=allowed_students)

    if status:
        qs = qs.filter(status=status)
    if student_id:
        qs = qs.filter(student_id=student_id)
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(summary__icontains=search))

    paginated = paginate_queryset(qs, page=page, page_size=page_size)

    items = []
    for c in paginated["items"]:
        # Find active class name from prefetched active enrollments
        active_enrs = getattr(c.student, "active_enrollments_list", [])
        active_enr = active_enrs[0] if active_enrs else None
        class_name = active_enr.school_class.name if active_enr else None

        items.append(
            StudentCaseItem(
                id=c.id,
                student_id=c.student.id,
                student_name=c.student.name,
                student_number=c.student.student_number,
                class_name=class_name,
                title=c.title,
                summary=c.summary,
                status=c.status,
                assigned_to_id=c.assigned_to_id,
                assigned_to_name=c.assigned_to.name if c.assigned_to else None,
                version=c.version,
                created_at=c.created_at,
            )
        )

    return StudentCaseListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def get_case_detail(case_id: int, actor: User) -> StudentCaseDetailResponse:
    require_roles(actor, ["Kesiswaan", "Wali Kelas"])

    case = StudentCase.objects.select_related("student", "assigned_to").filter(id=case_id).first()
    if not case:
        raise NotFoundError("Kasus kesiswaan tidak ditemukan.")

    user_roles = {r.name for r in actor.roles.all()}
    is_kesiswaan = "Kesiswaan" in user_roles

    if not is_kesiswaan:
        allowed_students = _get_accessible_student_ids(actor)
        if allowed_students is None or case.student_id not in allowed_students:
            raise PermissionDeniedError("Anda tidak memiliki wewenang membaca detail kasus siswa ini.")

    active_enr = case.student.enrollments.filter(end_date__isnull=True).select_related("school_class").first()
    class_name = active_enr.school_class.name if active_enr else None

    # Server-Side Response Filtering per DEC-TECH-18
    events = []
    for e in case.events.select_related("actor").order_by("created_at"):
        note = e.note
        if not is_kesiswaan and e.action == CaseActionEnum.CATAT_TINDAKAN:
            note = "[Catatan konseling privat - Terproteksi]"

        events.append(
            CaseEventItem(
                id=e.id,
                action=e.action,
                initial_status=e.initial_status,
                final_status=e.final_status,
                note=note,
                actor_id=e.actor_id,
                actor_name=e.actor.username,
                created_at=e.created_at,
            )
        )

    return StudentCaseDetailResponse(
        id=case.id,
        student_id=case.student.id,
        student_name=case.student.name,
        student_number=case.student.student_number,
        class_name=class_name,
        title=case.title,
        summary=case.summary,
        status=case.status,
        assigned_to_id=case.assigned_to_id,
        assigned_to_name=case.assigned_to.name if case.assigned_to else None,
        version=case.version,
        created_at=case.created_at,
        events=events,
    )
