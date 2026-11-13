from typing import Optional

from django.http import HttpRequest
from ninja import Query, Router
from ninja.responses import Response

from apps.core.security import jwt_auth, require_roles
from apps.student_affairs.schemas import (
    CaseTransitionRequest,
    CaseTransitionResponse,
    StudentCaseCreateRequest,
    StudentCaseDetailResponse,
    StudentCaseItem,
    StudentCaseListResponse,
)
from apps.student_affairs.selectors import get_case_detail, list_cases
from apps.student_affairs.services import create_case, transition_case

student_affairs_router = Router(tags=["Student Affairs"], auth=jwt_auth)


@student_affairs_router.get(
    "/cases",
    response={200: StudentCaseListResponse},
    operation_id="listStudentCases",
)
def get_cases(
    request: HttpRequest,
    status: Optional[str] = Query(None),
    student_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return list_cases(
        status=status,
        student_id=student_id,
        search=search,
        page=page,
        page_size=page_size,
        actor=request.user,
    )


@student_affairs_router.post(
    "/cases",
    response={201: StudentCaseItem},
    operation_id="createStudentCase",
)
def post_case(
    request: HttpRequest,
    payload: StudentCaseCreateRequest,
):
    require_roles(request.user, ["Kesiswaan", "Wali Kelas"])
    req_id = getattr(request, "request_id", None)
    case = create_case(payload, actor=request.user, request_id=req_id)
    detail = get_case_detail(case.id, actor=request.user)
    return Response(
        StudentCaseItem(
            id=detail.id,
            student_id=detail.student_id,
            student_name=detail.student_name,
            student_number=detail.student_number,
            class_name=detail.class_name,
            title=detail.title,
            summary=detail.summary,
            status=detail.status,
            assigned_to_id=detail.assigned_to_id,
            assigned_to_name=detail.assigned_to_name,
            version=detail.version,
            created_at=detail.created_at,
        ).model_dump(),
        status=201,
    )


@student_affairs_router.get(
    "/cases/{id}",
    response={200: StudentCaseDetailResponse},
    operation_id="getStudentCaseDetail",
)
def get_case(request: HttpRequest, id: int):
    require_roles(request.user, ["Kesiswaan", "Wali Kelas"])
    return get_case_detail(id, actor=request.user)


@student_affairs_router.post(
    "/cases/{id}/transitions",
    response={200: CaseTransitionResponse},
    operation_id="transitionStudentCase",
)
def post_transition(
    request: HttpRequest,
    id: int,
    payload: CaseTransitionRequest,
):
    require_roles(request.user, ["Kesiswaan"])
    req_id = getattr(request, "request_id", None)
    return transition_case(id, payload, actor=request.user, request_id=req_id)
