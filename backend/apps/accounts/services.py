import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone as dj_timezone

from apps.accounts.models import ActivityLog, Role, User, UserRole
from apps.accounts.schemas import LoginRequest, LoginResponse, RefreshResponse, UserCreateRequest, UserUpdateRequest
from apps.core.exceptions import (
    AuthenticationFailedError,
    BusinessValidationError,
    NotFoundError,
)
from apps.core.security import LoginRateLimiter
from apps.reports.services import invalidate_dashboard_cache


def issue_token_pair(user: User, family_id: Optional[str] = None) -> dict:
    now = datetime.now(UTC)

    # Roles union
    user_roles = list(user.roles.values_list("name", flat=True))

    access_jti = str(uuid.uuid4())
    access_payload = {
        "user_id": user.id,
        "username": user.username,
        "roles": user_roles,
        "token_type": "access",
        "jti": access_jti,
        "exp": now + timedelta(minutes=15),
        "iat": now,
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

    if not family_id:
        family_id = str(uuid.uuid4())

    refresh_jti = str(uuid.uuid4())
    refresh_payload = {
        "user_id": user.id,
        "token_type": "refresh",
        "jti": refresh_jti,
        "family_id": family_id,
        "exp": now + timedelta(days=7),
        "iat": now,
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 900,
    }


def authenticate_user(payload: LoginRequest, ip: str, request_id: Optional[str] = None) -> LoginResponse:
    LoginRateLimiter.check_rate_limit(ip, payload.username)

    user = User.objects.filter(username=payload.username).first()
    if not user or not user.check_password(payload.password):
        LoginRateLimiter.record_failure(ip, payload.username)
        ActivityLog.objects.create(
            actor=user,
            action="LOGIN_FAILED",
            resource_type="auth",
            request_id=request_id,
            ip_address=ip,
            metadata=f'{{"username_attempt": "{payload.username}"}}',
        )
        raise AuthenticationFailedError("Nama pengguna atau kata sandi tidak valid.")

    if not user.is_active:
        LoginRateLimiter.record_failure(ip, payload.username)
        ActivityLog.objects.create(
            actor=user,
            action="LOGIN_INACTIVE_BLOCKED",
            resource_type="auth",
            request_id=request_id,
            ip_address=ip,
        )
        raise AuthenticationFailedError("Akun pengguna telah dinonaktifkan.")

    # Successful login: reset rate limiter
    LoginRateLimiter.reset(ip, payload.username)

    user.last_login = dj_timezone.now()
    user.save(update_fields=["last_login"])

    tokens = issue_token_pair(user)

    ActivityLog.objects.create(
        actor=user,
        action="LOGIN_SUCCESS",
        resource_type="auth",
        request_id=request_id,
        ip_address=ip,
    )

    return LoginResponse(**tokens)


def rotate_refresh_token(refresh_token_str: str, ip: str, request_id: Optional[str] = None) -> RefreshResponse:
    try:
        payload = jwt.decode(
            refresh_token_str,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailedError("Token penyegaran telah kedaluwarsa.")
    except jwt.InvalidTokenError:
        raise AuthenticationFailedError("Token penyegaran tidak valid.")

    if payload.get("token_type") != "refresh":
        raise AuthenticationFailedError("Jenis token tidak valid.")

    jti = payload.get("jti")
    if not jti:
        raise AuthenticationFailedError("Identifier token tidak valid.")

    family_id = payload.get("family_id")
    if family_id:
        try:
            if cache.get(f"blacklist_family:{family_id}"):
                raise AuthenticationFailedError("Sesi token telah dicabut karena terdeteksi penyalahgunaan (reuse).")
        except AuthenticationFailedError:
            raise
        except Exception:
            raise AuthenticationFailedError("Layanan verifikasi sesi tidak tersedia (fail-closed).")

    try:
        is_blacklisted = bool(cache.get(f"blacklist:{jti}"))
    except Exception:
        raise AuthenticationFailedError("Layanan verifikasi sesi tidak tersedia (fail-closed).")

    if is_blacklisted:
        if family_id:
            try:
                cache.set(f"blacklist_family:{family_id}", True, timeout=7 * 86400)
            except Exception:
                pass
        raise AuthenticationFailedError("Token penyegaran tidak valid atau telah digunakan.")

    user_id = payload.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if not user or not user.is_active:
        raise AuthenticationFailedError("Pengguna tidak aktif atau tidak ditemukan.")

    # Blacklist old refresh token with fail-closed check
    try:
        cache.set(f"blacklist:{jti}", True, timeout=7 * 86400)
    except Exception:
        raise AuthenticationFailedError("Gagal mencatat pencabutan token (fail-closed).")

    # Issue new pair within same family
    tokens = issue_token_pair(user, family_id=family_id)

    ActivityLog.objects.create(
        actor=user,
        action="TOKEN_REFRESH",
        resource_type="auth",
        request_id=request_id,
        ip_address=ip,
    )

    return RefreshResponse(**tokens)


def revoke_token(
    refresh_token_str: str,
    actor: User,
    request_id: Optional[str] = None,
    access_jti: Optional[str] = None,
):
    if access_jti:
        try:
            cache.set(f"blacklist:{access_jti}", True, timeout=15 * 60)
        except Exception:
            pass

    try:
        payload = jwt.decode(
            refresh_token_str,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": False},
        )
        jti = payload.get("jti")
        if jti:
            cache.set(f"blacklist:{jti}", True, timeout=7 * 86400)
        family_id = payload.get("family_id")
        if family_id:
            cache.set(f"blacklist_family:{family_id}", True, timeout=7 * 86400)
    except Exception:
        pass

    ActivityLog.objects.create(
        actor=actor,
        action="LOGOUT",
        resource_type="auth",
        request_id=request_id,
    )


@transaction.atomic
def create_new_user(data: UserCreateRequest, actor: User) -> User:
    if User.objects.filter(username=data.username).exists():
        raise BusinessValidationError("Username sudah digunakan.")

    user = User.objects.create_user(
        username=data.username,
        password=data.password,
        is_active=data.is_active,
    )

    if data.roles:
        roles = Role.objects.filter(name__in=data.roles)
        for role in roles:
            UserRole.objects.create(user=user, role=role)

    ActivityLog.objects.create(
        actor=actor,
        action="CREATE_USER",
        resource_type="accounts",
        resource_id=str(user.id),
        metadata=f'{{"created_username": "{user.username}"}}',
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return user


@transaction.atomic
def update_existing_user(user_id: int, data: UserUpdateRequest, actor: User) -> User:
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise NotFoundError("Pengguna tidak ditemukan.")

    # Guard 1: Prevent self-deactivation
    if user.id == actor.id and data.is_active is False:
        raise BusinessValidationError("Anda tidak dapat menonaktifkan akun Anda sendiri.")

    # Guard 2: Prevent last active administrator lockout
    is_admin = user.roles.filter(name="Administrator").exists()
    if is_admin:
        active_admin_count = User.objects.filter(roles__name="Administrator", is_active=True).distinct().count()
        if active_admin_count <= 1:
            if data.is_active is False:
                raise BusinessValidationError("Tidak dapat menonaktifkan satu-satunya Administrator aktif di sistem.")
            if data.roles is not None and "Administrator" not in data.roles:
                raise BusinessValidationError(
                    "Tidak dapat menghapus peran Administrator dari satu-satunya Administrator aktif di sistem."
                )

    if data.is_active is not None:
        user.is_active = data.is_active

    if data.roles is not None:
        UserRole.objects.filter(user=user).delete()
        roles = Role.objects.filter(name__in=data.roles)
        for role in roles:
            UserRole.objects.create(user=user, role=role)

    user.save()

    ActivityLog.objects.create(
        actor=actor,
        action="UPDATE_USER",
        resource_type="accounts",
        resource_id=str(user.id),
    )
    transaction.on_commit(invalidate_dashboard_cache)
    return user
