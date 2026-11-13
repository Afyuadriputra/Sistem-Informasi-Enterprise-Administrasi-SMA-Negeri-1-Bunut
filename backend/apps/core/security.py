from typing import List, Optional

import jwt
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from ninja.security import HttpBearer

from apps.accounts.models import User
from apps.core.exceptions import AuthenticationFailedError, PermissionDeniedError, RateLimitExceededError


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[User]:
        if not token:
            raise AuthenticationFailedError("Token autentikasi tidak ditemukan.")

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailedError("Token autentikasi telah kedaluwarsa.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailedError("Token autentikasi tidak valid.")

        # Verify token type is access token
        token_type = payload.get("token_type")
        if token_type and token_type != "access":
            raise AuthenticationFailedError("Jenis token tidak valid.")

        jti = payload.get("jti")
        if jti and cache.get(f"blacklist:{jti}"):
            raise AuthenticationFailedError("Sesi token telah dicabut (logout).")

        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailedError("Identitas pengguna dalam token tidak valid.")

        try:
            user = User.objects.prefetch_related("roles").get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailedError("Pengguna tidak ditemukan.")

        if not user.is_active:
            raise AuthenticationFailedError("Akun pengguna telah dinonaktifkan.")

        request.user = user
        return user


jwt_auth = JWTAuth()


def check_roles(user: User, allowed_roles: List[str]) -> bool:
    """Evaluates multi-role union. Administrator has universal access."""
    if not user or not user.is_active:
        return False

    user_roles = {r.name for r in user.roles.all()}
    if "Administrator" in user_roles:
        return True

    return bool(user_roles.intersection(allowed_roles))


def require_roles(user: User, allowed_roles: List[str]):
    if not check_roles(user, allowed_roles):
        raise PermissionDeniedError("Anda tidak memiliki peran yang berwenang untuk operasi ini.")


class LoginRateLimiter:
    MAX_ATTEMPTS = 5
    WINDOW_SECONDS = 900  # 15 minutes

    @classmethod
    def _key(cls, ip: str, username: str) -> str:
        return f"ratelimit:login:{ip}:{username}"

    @classmethod
    def check_rate_limit(cls, ip: str, username: str):
        key = cls._key(ip, username)
        attempts = cache.get(key, 0)
        if attempts >= cls.MAX_ATTEMPTS:
            raise RateLimitExceededError(
                message="Terlalu banyak percobaan masuk yang gagal. Silakan coba 15 menit lagi.",
                retry_after=cls.WINDOW_SECONDS,
            )

    @classmethod
    def record_failure(cls, ip: str, username: str):
        key = cls._key(ip, username)
        attempts = cache.get(key, 0)
        cache.set(key, attempts + 1, timeout=cls.WINDOW_SECONDS)

    @classmethod
    def reset(cls, ip: str, username: str):
        key = cls._key(ip, username)
        cache.delete(key)


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "127.0.0.1")
