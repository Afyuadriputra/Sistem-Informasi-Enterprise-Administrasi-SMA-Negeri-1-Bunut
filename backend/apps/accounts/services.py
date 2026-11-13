import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from django.core.cache import cache
from django.db import transaction

from apps.accounts.models import ActivityLog, Role, User, UserRole
from apps.accounts.schemas import LoginRequest, LoginResponse, RefreshResponse, UserCreateRequest, UserUpdateRequest
from apps.core.exceptions import AuthenticationFailedError, BusinessValidationError, NotFoundError
from apps.core.security import LoginRateLimiter


def issue_token_pair(user: User) -> dict:
    now = datetime.now(UTC)
    access_jti = uuid.uuid4().hex
    refresh_jti = uuid.uuid4().hex

    roles = [r.name for r in user.roles.all()]

    access_payload = {
        "user_id": user.id,
        "username": user.username,
        "roles": roles,
        "token_type": "access",
        "jti": access_jti,
        "exp": now + timedelta(minutes=15),
        "iat": now,
    }

    refresh_payload = {
        "user_id": user.id,
        "username": user.username,
        "token_type": "refresh",
        "jti": refresh_jti,
        "exp": now + timedelta(days=7),
        "iat": now,
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 900,
    }


def authenticate_user(
    payload: LoginRequest, ip: str, request_id: Optional[str] = None
) -> LoginResponse:
    LoginRateLimiter.check_rate_limit(ip, payload.username)

    user = User.objects.filter(username=payload.username).first()

    if not user or not user.check_password(payload.password):
        LoginRateLimiter.record_failure(ip, payload.username)
        ActivityLog.objects.create(
            actor=None,
            action="LOGIN_FAILED",
            resource_type="auth",
            request_id=request_id,
            ip_address=ip,
            metadata=f'{{"username": "{payload.username}"}}',
        )
        raise AuthenticationFailedError("Kredensial tidak valid.")

    if not user.is_active:
        LoginRateLimiter.record_failure(ip, payload.username)
        ActivityLog.objects.create(
            actor=user,
            action="LOGIN_FAILED_INACTIVE",
            resource_type="auth",
            request_id=request_id,
            ip_address=ip,
        )
        raise AuthenticationFailedError("Akun pengguna telah dinonaktifkan.")

    # Successful login
    LoginRateLimiter.reset(ip, payload.username)
    tokens = issue_token_pair(user)

    ActivityLog.objects.create(
        actor=user,
        action="LOGIN_SUCCESS",
        resource_type="auth",
        request_id=request_id,
        ip_address=ip,
    )

    return LoginResponse(**tokens)


def rotate_refresh_token(
    refresh_token_str: str, ip: str, request_id: Optional[str] = None
) -> RefreshResponse:
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
    if not jti or cache.get(f"blacklist:{jti}"):
        raise AuthenticationFailedError("Token penyegaran tidak valid atau telah digunakan.")

    user_id = payload.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if not user or not user.is_active:
        raise AuthenticationFailedError("Pengguna tidak aktif atau tidak ditemukan.")

    # Blacklist old refresh token (7 days TTL)
    cache.set(f"blacklist:{jti}", True, timeout=7 * 86400)

    # Issue new pair
    tokens = issue_token_pair(user)

    ActivityLog.objects.create(
        actor=user,
        action="TOKEN_REFRESH",
        resource_type="auth",
        request_id=request_id,
        ip_address=ip,
    )

    return RefreshResponse(**tokens)


def revoke_token(
    refresh_token_str: str, actor: User, request_id: Optional[str] = None
):
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
    return user


@transaction.atomic
def update_existing_user(user_id: int, data: UserUpdateRequest, actor: User) -> User:
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise NotFoundError("Pengguna tidak ditemukan.")

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
    return user
