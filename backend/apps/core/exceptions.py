from typing import List


class AppException(Exception):
    status_code: int = 500
    code: str = "INTERNAL_SERVER_ERROR"

    def __init__(
        self,
        message: str = "Terjadi kesalahan internal pada server.",
        details: List[dict] | None = None,
        status_code: int | None = None,
        code: str | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.details = details or []
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code


class BusinessValidationError(AppException):
    status_code = 422
    code = "VALIDATION_ERROR"

    def __init__(
        self,
        message: str = "Data yang dimasukkan tidak memenuhi ketentuan.",
        details: List[dict] | None = None,
    ):
        super().__init__(message=message, details=details, status_code=422, code="VALIDATION_ERROR")


class AuthenticationFailedError(AppException):
    status_code = 401
    code = "AUTHENTICATION_FAILED"

    def __init__(
        self,
        message: str = "Kredensial tidak valid.",
        details: List[dict] | None = None,
    ):
        super().__init__(message=message, details=details, status_code=401, code="AUTHENTICATION_FAILED")


class PermissionDeniedError(AppException):
    status_code = 403
    code = "PERMISSION_DENIED"

    def __init__(
        self,
        message: str = "Anda tidak memiliki wewenang untuk mengakses sumber daya ini.",
        details: List[dict] | None = None,
    ):
        super().__init__(message=message, details=details, status_code=403, code="PERMISSION_DENIED")


class NotFoundError(AppException):
    status_code = 404
    code = "NOT_FOUND"

    def __init__(
        self,
        message: str = "Data atau sumber daya yang diminta tidak ditemukan.",
        details: List[dict] | None = None,
    ):
        super().__init__(message=message, details=details, status_code=404, code="NOT_FOUND")


class ConcurrencyConflictError(AppException):
    status_code = 409
    code = "CONCURRENCY_CONFLICT"

    def __init__(
        self,
        message: str = "Data telah diperbarui oleh pengguna lain. Silakan muat ulang halaman.",
        details: List[dict] | None = None,
    ):
        super().__init__(message=message, details=details, status_code=409, code="CONCURRENCY_CONFLICT")


class RateLimitExceededError(AppException):
    status_code = 429
    code = "RATE_LIMIT_EXCEEDED"

    def __init__(
        self,
        message: str = "Terlalu banyak percobaan. Silakan coba beberapa saat lagi.",
        details: List[dict] | None = None,
        retry_after: int = 900,
    ):
        super().__init__(message=message, details=details, status_code=429, code="RATE_LIMIT_EXCEEDED")
        self.retry_after = retry_after
