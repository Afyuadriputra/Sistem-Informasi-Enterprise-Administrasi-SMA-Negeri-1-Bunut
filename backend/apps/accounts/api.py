from typing import Optional

from django.http import HttpRequest
from ninja import Query, Router

from apps.accounts.schemas import (
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    RefreshRequest,
    RefreshResponse,
    RoleListResponse,
    UserCreateRequest,
    UserItem,
    UserListResponse,
    UserProfileResponse,
    UserUpdateRequest,
)
from apps.accounts.selectors import get_user_detail, get_user_profile, list_roles, list_users
from apps.accounts.services import (
    authenticate_user,
    create_new_user,
    revoke_token,
    rotate_refresh_token,
    update_existing_user,
)
from apps.core.schemas import SuccessMessageResponse
from apps.core.security import get_client_ip, jwt_auth, require_roles

auth_router = Router(tags=["Auth"])
accounts_router = Router(tags=["Accounts"], auth=jwt_auth)


@auth_router.post("/login", response={200: LoginResponse}, operation_id="authLogin")
def login(request: HttpRequest, payload: LoginRequest):
    ip = get_client_ip(request)
    req_id = getattr(request, "request_id", None)
    return authenticate_user(payload, ip, req_id)


@auth_router.post("/refresh", response={200: RefreshResponse}, operation_id="authRefresh")
def refresh(request: HttpRequest, payload: RefreshRequest):
    ip = get_client_ip(request)
    req_id = getattr(request, "request_id", None)
    return rotate_refresh_token(payload.refresh_token, ip, req_id)


@auth_router.post(
    "/logout",
    auth=jwt_auth,
    response={200: SuccessMessageResponse},
    operation_id="authLogout",
)
def logout(request: HttpRequest, payload: LogoutRequest):
    req_id = getattr(request, "request_id", None)
    access_jti = getattr(request, "token_jti", None)
    revoke_token(payload.refresh_token, request.user, req_id, access_jti=access_jti)
    return SuccessMessageResponse(message="Sesi berhasil diakhiri.")


@auth_router.get(
    "/me",
    auth=jwt_auth,
    response={200: UserProfileResponse},
    operation_id="authMe",
)
def me(request: HttpRequest):
    return get_user_profile(request.user)


@accounts_router.get(
    "/users",
    response={200: UserListResponse},
    operation_id="listUsers",
)
def get_users(
    request: HttpRequest,
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    require_roles(request.user, ["Administrator"])
    return list_users(
        search=search,
        role=role,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )


@accounts_router.post(
    "/users",
    response={201: UserItem},
    operation_id="createUser",
)
def create_user_endpoint(request: HttpRequest, payload: UserCreateRequest):
    require_roles(request.user, ["Administrator"])
    user = create_new_user(payload, actor=request.user)
    from ninja.responses import Response

    return Response(get_user_detail(user.id).model_dump(), status=201)


@accounts_router.get(
    "/users/{id}",
    response={200: UserItem},
    operation_id="getUserDetail",
)
def get_user_endpoint(request: HttpRequest, id: int):
    require_roles(request.user, ["Administrator"])
    return get_user_detail(id)


@accounts_router.patch(
    "/users/{id}",
    response={200: UserItem},
    operation_id="updateUser",
)
def update_user_endpoint(request: HttpRequest, id: int, payload: UserUpdateRequest):
    require_roles(request.user, ["Administrator"])
    user = update_existing_user(id, payload, actor=request.user)
    return get_user_detail(user.id)


@accounts_router.get(
    "/roles",
    response={200: RoleListResponse},
    operation_id="listRoles",
)
def get_roles(request: HttpRequest):
    require_roles(request.user, ["Administrator"])
    return list_roles()
