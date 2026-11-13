import logging
import uuid

from django.conf import settings
from django.db import OperationalError
from django.http import HttpRequest, JsonResponse
from ninja import NinjaAPI
from ninja.errors import HttpError
from ninja.errors import ValidationError as NinjaValidationError
from pydantic import ValidationError as PydanticValidationError

from apps.core.exceptions import AppException

logger = logging.getLogger("api.errors")

api = NinjaAPI(
    title="API Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut",
    version="1.1.0",
    description=(
        "Kontrak API REST resmi untuk integrasi antarmuka web SPA dan layanan backend "
        "Django Ninja (Baseline M0.2, 49 Operasi, 71 Skema)."
    ),
    urls_namespace="api",
    docs_url="/docs" if settings.DEBUG else None,
)


def get_request_id(request: HttpRequest) -> str:
    req_id = getattr(request, "request_id", None)
    if not req_id:
        req_id = request.headers.get("X-Request-ID")
    if not req_id:
        req_id = f"req-{uuid.uuid4().hex[:16]}"
        request.request_id = req_id
    return req_id


@api.exception_handler(AppException)
def app_exception_handler(request: HttpRequest, exc: AppException):
    req_id = get_request_id(request)
    payload = {
        "code": exc.code,
        "message": exc.message,
        "details": exc.details if exc.details else None,
        "request_id": req_id,
    }
    response = JsonResponse(payload, status=exc.status_code)
    response["X-Request-ID"] = req_id
    if hasattr(exc, "retry_after"):
        response["Retry-After"] = str(exc.retry_after)
    return response


@api.exception_handler(NinjaValidationError)
def ninja_validation_error_handler(request: HttpRequest, exc: NinjaValidationError):
    req_id = get_request_id(request)
    details = []
    for err in exc.errors:
        field = None
        if "loc" in err and len(err["loc"]) > 0:
            field = str(err["loc"][-1])
        msg = err.get("msg", "Nilai tidak valid")
        details.append({"field": field, "message": msg})

    payload = {
        "code": "VALIDATION_ERROR",
        "message": "Data yang dimasukkan tidak memenuhi ketentuan.",
        "details": details if details else None,
        "request_id": req_id,
    }
    response = JsonResponse(payload, status=422)
    response["X-Request-ID"] = req_id
    return response


@api.exception_handler(PydanticValidationError)
def pydantic_validation_error_handler(request: HttpRequest, exc: PydanticValidationError):
    req_id = get_request_id(request)
    details = []
    for err in exc.errors():
        field = None
        if "loc" in err and len(err["loc"]) > 0:
            field = str(err["loc"][-1])
        msg = err.get("msg", "Nilai tidak valid")
        details.append({"field": field, "message": msg})

    payload = {
        "code": "VALIDATION_ERROR",
        "message": "Data yang dimasukkan tidak memenuhi ketentuan.",
        "details": details if details else None,
        "request_id": req_id,
    }
    response = JsonResponse(payload, status=422)
    response["X-Request-ID"] = req_id
    return response


@api.exception_handler(HttpError)
def http_error_handler(request: HttpRequest, exc: HttpError):
    req_id = get_request_id(request)
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "PERMISSION_DENIED",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONCURRENCY_CONFLICT",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
    }
    payload = {
        "code": code_map.get(exc.status_code, "HTTP_ERROR"),
        "message": str(exc.message or "Terjadi kesalahan pada permintaan."),
        "details": None,
        "request_id": req_id,
    }
    response = JsonResponse(payload, status=exc.status_code)
    response["X-Request-ID"] = req_id
    return response


@api.exception_handler(OperationalError)
def operational_error_handler(request: HttpRequest, exc: OperationalError):
    if "locked" in str(exc).lower():
        req_id = get_request_id(request)
        payload = {
            "code": "CONCURRENCY_CONFLICT",
            "message": "Terjadi konflik konkurensi saat mengakses basis data. Silakan coba kembali.",
            "details": None,
            "request_id": req_id,
        }
        response = JsonResponse(payload, status=409)
        response["X-Request-ID"] = req_id
        return response
    return generic_exception_handler(request, exc)


@api.exception_handler(Exception)
def generic_exception_handler(request: HttpRequest, exc: Exception):
    req_id = get_request_id(request)
    logger.exception(f"Unhandled exception on {request.path} [req: {req_id}]: {exc}")
    payload = {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Terjadi kesalahan internal pada server.",
        "details": None,
        "request_id": req_id,
    }
    response = JsonResponse(payload, status=500)
    response["X-Request-ID"] = req_id
    return response


@api.get("/health", tags=["System"], response={200: dict})
def health_check(request: HttpRequest):
    """Healthcheck endpoint for infrastructure monitoring"""
    return {
        "status": "ok",
        "version": "1.1.0",
        "service": "sie-sman1-bunut-backend",
    }


# Mount Routers
from apps.accounts.api import accounts_router, auth_router
from apps.administration.api import administration_router
from apps.attendance.api import attendance_router
from apps.master_data.api import master_router
from apps.reports.api import audit_router, reports_router
from apps.student_affairs.api import student_affairs_router

api.add_router("/auth", auth_router)
api.add_router("/accounts", accounts_router)
api.add_router("/master", master_router)
api.add_router("/attendance", attendance_router)
api.add_router("/student-affairs", student_affairs_router)
api.add_router("/administration", administration_router)
api.add_router("/reports", reports_router)
api.add_router("/audit-logs", audit_router)
