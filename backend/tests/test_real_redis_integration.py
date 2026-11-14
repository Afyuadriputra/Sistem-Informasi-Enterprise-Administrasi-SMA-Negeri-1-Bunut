import socket
import pytest
from django.core.cache.backends.redis import RedisCache
from django.test import Client

from apps.accounts.models import Role, User, UserRole
from apps.accounts.services import issue_token_pair
from apps.core.exceptions import RateLimitExceededError
from apps.core.security import LoginRateLimiter


def is_redis_available():
    s = socket.socket()
    s.settimeout(1.0)
    try:
        s.connect(("127.0.0.1", 6379))
        s.sendall(b"PING\r\n")
        res = s.recv(1024)
        return b"+PONG" in res
    except Exception:
        return False
    finally:
        s.close()


@pytest.fixture
def redis_cache():
    if not is_redis_available():
        pytest.skip("Real Redis is not available on 127.0.0.1:6379")
    cache = RedisCache("redis://127.0.0.1:6379/2", {"KEY_PREFIX": "sie_test_integration"})
    yield cache
    # Clean up only keys in this test db
    try:
        client = cache.get_client()
        keys = client.keys("sie_test_integration:*")
        if keys:
            client.delete(*keys)
    except Exception:
        pass


@pytest.mark.django_db
def test_real_redis_login_rate_limiter_shared_state(redis_cache, monkeypatch):
    """Verify that LoginRateLimiter uses Redis shared state for brute-force tracking."""
    monkeypatch.setattr("apps.core.security.cache", redis_cache)
    monkeypatch.setattr("apps.accounts.services.cache", redis_cache)

    ip = "192.168.1.100"
    username = "target_user"

    # Reset before test
    LoginRateLimiter.reset(ip, username)

    # 4 failed attempts recorded
    for i in range(4):
        LoginRateLimiter.record_failure(ip, username)
        LoginRateLimiter.check_rate_limit(ip, username)  # Should not raise

    # 5th failed attempt
    LoginRateLimiter.record_failure(ip, username)

    # 6th check must raise RateLimitExceededError
    with pytest.raises(RateLimitExceededError) as exc_info:
        LoginRateLimiter.check_rate_limit(ip, username)

    assert exc_info.value.retry_after == 900
    LoginRateLimiter.reset(ip, username)


@pytest.mark.django_db
def test_real_redis_multi_worker_session_revocation(redis_cache, monkeypatch):
    """Multi-worker test:
    Worker A issues tokens and logs out.
    Worker B (independent client) must immediately reject the revoked token from shared Redis state.
    """
    monkeypatch.setattr("apps.core.security.cache", redis_cache)
    monkeypatch.setattr("apps.accounts.services.cache", redis_cache)

    admin_role = Role.objects.create(name="Administrator")
    user = User.objects.create_user(username="redis_worker_user", password="Password123!")
    UserRole.objects.create(user=user, role=admin_role)

    # Worker A: User logs in
    worker_a = Client()
    login_res = worker_a.post(
        "/api/auth/login",
        data={"username": "redis_worker_user", "password": "Password123!"},
        content_type="application/json",
    )
    assert login_res.status_code == 200
    tokens = login_res.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # Worker B: Access protected route using token from Worker A
    worker_b = Client()
    headers_b = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    me_res_b = worker_b.get("/api/auth/me", **headers_b)
    assert me_res_b.status_code == 200
    assert me_res_b.json()["username"] == "redis_worker_user"

    # Worker A: Logout and revoke session
    logout_res = worker_a.post(
        "/api/auth/logout",
        data={"refresh_token": refresh_token},
        content_type="application/json",
        **{"HTTP_AUTHORIZATION": f"Bearer {access_token}"},
    )
    assert logout_res.status_code == 200

    # Worker B: Subsequent call with the same access token must be REJECTED via shared Redis blacklist
    me_after_logout_b = worker_b.get("/api/auth/me", **headers_b)
    assert me_after_logout_b.status_code == 401
    assert me_after_logout_b.json()["code"] == "AUTHENTICATION_FAILED"


@pytest.mark.django_db
def test_real_redis_token_family_reuse_invalidation(redis_cache, monkeypatch):
    """Verify that reusing an already rotated refresh token revokes the entire token family in Redis."""
    monkeypatch.setattr("apps.core.security.cache", redis_cache)
    monkeypatch.setattr("apps.accounts.services.cache", redis_cache)

    admin_role = Role.objects.create(name="Administrator")
    user = User.objects.create_user(username="family_reuse_user", password="Password123!")
    UserRole.objects.create(user=user, role=admin_role)

    client = Client()

    # 1. First token pair
    pair_1 = issue_token_pair(user)
    refresh_1 = pair_1["refresh_token"]

    # 2. Legitimate rotation: use refresh_1 to get pair_2
    rot_res = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_1},
        content_type="application/json",
    )
    assert rot_res.status_code == 200
    pair_2 = rot_res.json()
    refresh_2 = pair_2["refresh_token"]

    # 3. Attacker replays refresh_1 (token reuse detection)
    replay_res = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_1},
        content_type="application/json",
    )
    assert replay_res.status_code == 401
    assert "telah digunakan" in replay_res.json()["message"].lower()

    # 4. Legit user now attempts to use refresh_2 -> must be BLOCKED because family was invalidated in Redis
    subsequent_res = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_2},
        content_type="application/json",
    )
    assert subsequent_res.status_code == 401
    assert "reuse" in subsequent_res.json()["message"].lower() or "dicabut" in subsequent_res.json()["message"].lower()


@pytest.mark.django_db
def test_real_redis_cross_worker_rate_limiting(redis_cache, monkeypatch):
    """Cross-worker brute-force tracking:
    Failed logins on Worker A count against the limit on Worker B.
    """
    monkeypatch.setattr("apps.core.security.cache", redis_cache)
    monkeypatch.setattr("apps.accounts.services.cache", redis_cache)

    user = User.objects.create_user(username="victim_user", password="Password123!")
    Role.objects.create(name="Administrator")

    worker_a = Client(REMOTE_ADDR="10.0.0.1")
    worker_b = Client(REMOTE_ADDR="10.0.0.1")

    LoginRateLimiter.reset("10.0.0.1", "victim_user")

    # 3 failed logins on Worker A
    for _ in range(3):
        r = worker_a.post(
            "/api/auth/login",
            data={"username": "victim_user", "password": "WrongPassword!"},
            content_type="application/json",
        )
        assert r.status_code == 401

    # 2 failed logins on Worker B
    for _ in range(2):
        r = worker_b.post(
            "/api/auth/login",
            data={"username": "victim_user", "password": "WrongPassword!"},
            content_type="application/json",
        )
        assert r.status_code == 401

    # 6th attempt on Worker B must be rate-limited (HTTP 429)
    blocked_res = worker_b.post(
        "/api/auth/login",
        data={"username": "victim_user", "password": "Password123!"},
        content_type="application/json",
    )
    assert blocked_res.status_code == 429
    assert blocked_res.json()["code"] == "RATE_LIMIT_EXCEEDED"

    LoginRateLimiter.reset("10.0.0.1", "victim_user")
