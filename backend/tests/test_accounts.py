import pytest
from django.core.cache import cache
from django.test import Client

from apps.accounts.models import Role, User, UserRole


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def sample_roles(db):
    admin_role = Role.objects.create(name="Administrator", description="Admin Sistem")
    guru_role = Role.objects.create(name="Guru", description="Guru Pengampu")
    wali_role = Role.objects.create(name="Wali Kelas", description="Wali Kelas")
    return {
        "admin": admin_role,
        "guru": guru_role,
        "wali": wali_role,
    }


@pytest.fixture
def admin_user(db, sample_roles):
    user = User.objects.create_user(username="admin_test", password="Password123!")
    UserRole.objects.create(user=user, role=sample_roles["admin"])
    return user


@pytest.fixture
def guru_user(db, sample_roles):
    user = User.objects.create_user(username="guru_test", password="Password123!")
    UserRole.objects.create(user=user, role=sample_roles["guru"])
    return user


@pytest.fixture
def inactive_user(db, sample_roles):
    user = User.objects.create_user(username="inactive_test", password="Password123!", is_active=False)
    UserRole.objects.create(user=user, role=sample_roles["guru"])
    return user


@pytest.mark.django_db
def test_valid_login(client: Client, guru_user):
    """Test successful login with valid credentials."""
    response = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "Password123!"},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] == 900


@pytest.mark.django_db
def test_invalid_login_credentials(client: Client, guru_user):
    """Test invalid password returns 401 and standard error envelope."""
    response = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "WrongPassword!"},
        content_type="application/json",
    )
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == "AUTHENTICATION_FAILED"
    assert "X-Request-ID" in response.headers


@pytest.mark.django_db
def test_rate_limiting_brute_force_be_01(client: Client, guru_user):
    """BE-01: 5 consecutive failed attempts trigger HTTP 429 Too Many Requests."""
    for _ in range(5):
        res = client.post(
            "/api/auth/login",
            data={"username": "guru_test", "password": "BadPassword!"},
            content_type="application/json",
        )
        assert res.status_code == 401

    # 6th attempt must be blocked by rate limiter
    res_blocked = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "Password123!"},
        content_type="application/json",
    )
    assert res_blocked.status_code == 429
    assert res_blocked.json()["code"] == "RATE_LIMIT_EXCEEDED"
    assert "Retry-After" in res_blocked.headers


@pytest.mark.django_db
def test_inactive_account_rejected_be_02(client: Client, guru_user):
    """BE-02: Deactivated account is immediately rejected on token use."""
    # Step 1: Login while active
    login_res = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "Password123!"},
        content_type="application/json",
    )
    assert login_res.status_code == 200
    access_token = login_res.json()["access_token"]

    # Step 2: Verify active user can access /auth/me
    auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    me_res = client.get("/api/auth/me", **auth_headers)
    assert me_res.status_code == 200

    # Step 3: Deactivate user
    guru_user.is_active = False
    guru_user.save()

    # Step 4: Token must be rejected
    me_rejected = client.get("/api/auth/me", **auth_headers)
    assert me_rejected.status_code == 401
    assert me_rejected.json()["code"] == "AUTHENTICATION_FAILED"


@pytest.mark.django_db
def test_refresh_token_rotation_and_reuse_prevention(client: Client, guru_user):
    """Test refresh rotation and rejection of already-used refresh token."""
    login_res = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "Password123!"},
        content_type="application/json",
    )
    refresh_token = login_res.json()["refresh_token"]

    # Rotate refresh token
    refresh_res = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_token},
        content_type="application/json",
    )
    assert refresh_res.status_code == 200
    new_refresh_token = refresh_res.json()["refresh_token"]
    assert new_refresh_token != refresh_token

    # Reusing the old refresh token must fail
    reuse_res = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_token},
        content_type="application/json",
    )
    assert reuse_res.status_code == 401


@pytest.mark.django_db
def test_logout_session_revocation(client: Client, guru_user):
    """Test logout blacklists refresh token."""
    login_res = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "Password123!"},
        content_type="application/json",
    )
    access_token = login_res.json()["access_token"]
    refresh_token = login_res.json()["refresh_token"]

    logout_res = client.post(
        "/api/auth/logout",
        data={"refresh_token": refresh_token},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )
    assert logout_res.status_code == 200

    # Attempt to refresh with logged-out token must fail
    fail_res = client.post(
        "/api/auth/refresh",
        data={"refresh_token": refresh_token},
        content_type="application/json",
    )
    assert fail_res.status_code == 401


@pytest.mark.django_db
def test_accounts_crud_and_rbac(client: Client, admin_user, guru_user):
    """Test accounts management is restricted to Administrator."""
    # Login as admin
    admin_login = client.post(
        "/api/auth/login",
        data={"username": "admin_test", "password": "Password123!"},
        content_type="application/json",
    )
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {admin_token}"}

    # Login as guru
    guru_login = client.post(
        "/api/auth/login",
        data={"username": "guru_test", "password": "Password123!"},
        content_type="application/json",
    )
    guru_token = guru_login.json()["access_token"]
    guru_headers = {"HTTP_AUTHORIZATION": f"Bearer {guru_token}"}

    # Guru trying to access /accounts/users -> 403 Forbidden
    forbidden_res = client.get("/api/accounts/users", **guru_headers)
    assert forbidden_res.status_code == 403

    # Admin accessing /accounts/users -> 200 OK
    list_res = client.get("/api/accounts/users", **admin_headers)
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 2

    # Admin creates new user
    create_res = client.post(
        "/api/accounts/users",
        data={
            "username": "kesiswaan_new",
            "password": "Password123!",
            "roles": ["Administrator"],
            "is_active": True,
        },
        content_type="application/json",
        **admin_headers,
    )
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # Admin gets user detail
    detail_res = client.get(f"/api/accounts/users/{created_id}", **admin_headers)
    assert detail_res.status_code == 200
    assert detail_res.json()["username"] == "kesiswaan_new"

    # Admin updates user
    update_res = client.patch(
        f"/api/accounts/users/{created_id}",
        data={"is_active": False},
        content_type="application/json",
        **admin_headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["is_active"] is False
