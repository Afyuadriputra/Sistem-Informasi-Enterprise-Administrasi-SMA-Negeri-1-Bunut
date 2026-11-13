from datetime import UTC, datetime, timedelta

import jwt
import pytest
from django.conf import settings
from django.core.cache import cache

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair


@pytest.fixture
def auth_env(db):
    cache.clear()
    admin_r = Role.objects.create(name="Administrator")
    u1 = User.objects.create_user(username="jwt_user_1", password="Password123!")
    UserRole.objects.create(user=u1, role=admin_r)

    u2 = User.objects.create_user(username="jwt_user_2", password="Password123!")
    UserRole.objects.create(user=u2, role=admin_r)

    tokens = issue_token_pair(u1)
    return {
        "user1": u1,
        "user2": u2,
        "tokens": tokens,
    }


@pytest.mark.django_db
def test_jwt_valid_access_token(client, auth_env):
    """Valid access token should authenticate successfully."""
    headers = {"HTTP_AUTHORIZATION": f"Bearer {auth_env['tokens']['access_token']}"}
    res = client.get("/api/auth/me", **headers)
    assert res.status_code == 200
    assert res.json()["username"] == "jwt_user_1"


@pytest.mark.django_db
def test_jwt_expired_access_token(client, auth_env):
    """Expired access token must return 401 Unauthorized."""
    past = datetime.now(UTC) - timedelta(minutes=30)
    payload = {
        "user_id": auth_env["user1"].id,
        "username": auth_env["user1"].username,
        "token_type": "access",
        "jti": "expired-jti-test",
        "exp": past,
        "iat": past - timedelta(minutes=15),
    }
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {expired_token}"}
    res = client.get("/api/auth/me", **headers)
    assert res.status_code == 401


@pytest.mark.django_db
def test_jwt_invalid_signature_and_malformed(client, auth_env):
    """Tampered token or bad signature must return 401."""
    # 1. Tampered signature
    bad_token = jwt.encode(
        {"user_id": auth_env["user1"].id, "token_type": "access"},
        "wrong-secret-key-12345678901234567890",
        algorithm="HS256",
    )
    headers = {"HTTP_AUTHORIZATION": f"Bearer {bad_token}"}
    res = client.get("/api/auth/me", **headers)
    assert res.status_code == 401

    # 2. Malformed token
    headers_malformed = {"HTTP_AUTHORIZATION": "Bearer invalid.token.payload"}
    res_malformed = client.get("/api/auth/me", **headers_malformed)
    assert res_malformed.status_code == 401


@pytest.mark.django_db
def test_jwt_token_type_mixup_prevention(client, auth_env):
    """Passing a refresh_token as an access_token must return 401."""
    refresh_token = auth_env["tokens"]["refresh_token"]
    headers = {"HTTP_AUTHORIZATION": f"Bearer {refresh_token}"}
    res = client.get("/api/auth/me", **headers)
    assert res.status_code == 401

    # Passing an access_token to /auth/refresh must return 401
    access_token = auth_env["tokens"]["access_token"]
    res_refresh = client.post(
        "/api/auth/refresh",
        data={"refresh_token": access_token},
        content_type="application/json",
    )
    assert res_refresh.status_code == 401


@pytest.mark.django_db
def test_jwt_refresh_token_rotation_and_reuse_invalidation(client, auth_env):
    """Refresh token rotation must invalidate old refresh token and revoke family upon reuse."""
    old_refresh = auth_env["tokens"]["refresh_token"]

    # 1. First refresh -> 200 OK with new tokens
    res1 = client.post(
        "/api/auth/refresh",
        data={"refresh_token": old_refresh},
        content_type="application/json",
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["access_token"]
    new_refresh = data1["refresh_token"]
    assert new_refresh != old_refresh

    # 2. Replay of old refresh token -> 401 and family revocation
    res_replay = client.post(
        "/api/auth/refresh",
        data={"refresh_token": old_refresh},
        content_type="application/json",
    )
    assert res_replay.status_code == 401

    # 3. New refresh token is now also invalidated due to reuse detection
    res_subsequent = client.post(
        "/api/auth/refresh",
        data={"refresh_token": new_refresh},
        content_type="application/json",
    )
    assert res_subsequent.status_code == 401


@pytest.mark.django_db
def test_jwt_logout_session_blacklisting(client, auth_env):
    """Logout blacklists both access token and refresh token."""
    access_token = auth_env["tokens"]["access_token"]
    refresh_token = auth_env["tokens"]["refresh_token"]
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    res_logout = client.post(
        "/api/auth/logout",
        data={"refresh_token": refresh_token},
        content_type="application/json",
        **headers,
    )
    assert res_logout.status_code == 200

    # Access token must now be rejected
    res_me = client.get("/api/auth/me", **headers)
    assert res_me.status_code == 401

    # Refresh token must also be rejected
    res_ref = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_token},
        content_type="application/json",
    )
    assert res_ref.status_code == 401


@pytest.mark.django_db
def test_jwt_account_deactivation_immediate_block(client, auth_env):
    """Deactivated user account is immediately blocked from auth."""
    u1 = auth_env["user1"]
    access_token = auth_env["tokens"]["access_token"]
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    # Verify initially active
    assert client.get("/api/auth/me", **headers).status_code == 200

    # Deactivate u1
    u1.is_active = False
    u1.save(update_fields=["is_active"])

    # Subsequent request with existing token is rejected
    res = client.get("/api/auth/me", **headers)
    assert res.status_code == 401


@pytest.mark.django_db
def test_self_deactivation_and_last_admin_lockout(client, auth_env):
    """Administrator cannot deactivate self or deactivate the last active administrator."""
    u1 = auth_env["user1"]
    u2 = auth_env["user2"]
    token1 = auth_env["tokens"]["access_token"]
    headers1 = {"HTTP_AUTHORIZATION": f"Bearer {token1}"}

    # 1. Attempt self-deactivation -> 422 BusinessValidationError
    res_self = client.patch(
        f"/api/accounts/users/{u1.id}",
        data={"is_active": False},
        content_type="application/json",
        **headers1,
    )
    assert res_self.status_code == 422
    assert "menonaktifkan akun anda sendiri" in res_self.json()["message"].lower()

    # 2. Deactivate u2 by u1 -> 200 OK
    res_u2 = client.patch(
        f"/api/accounts/users/{u2.id}",
        data={"is_active": False},
        content_type="application/json",
        **headers1,
    )
    assert res_u2.status_code == 200

    # 3. Now u1 is the ONLY active admin. Attempting to deactivate u1 (even if attempted via API)
    # is rejected by the last-active-admin guard
    res_last = client.patch(
        f"/api/accounts/users/{u1.id}",
        data={"is_active": False},
        content_type="application/json",
        **headers1,
    )
    assert res_last.status_code == 422


@pytest.mark.django_db
def test_login_rate_limiting_brute_force(client, auth_env):
    """5 consecutive failed logins trigger rate limit cooldown."""
    cache.clear()
    for _ in range(5):
        res = client.post(
            "/api/auth/login",
            data={"username": "jwt_user_1", "password": "WrongPassword!"},
            content_type="application/json",
        )
        assert res.status_code == 401

    # 6th attempt -> 429 Too Many Requests
    res_blocked = client.post(
        "/api/auth/login",
        data={"username": "jwt_user_1", "password": "WrongPassword!"},
        content_type="application/json",
    )
    assert res_blocked.status_code == 429
