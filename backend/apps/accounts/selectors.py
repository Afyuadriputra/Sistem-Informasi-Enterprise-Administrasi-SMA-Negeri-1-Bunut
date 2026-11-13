from typing import Optional

from apps.accounts.models import Role, User
from apps.accounts.schemas import RoleItem, RoleListResponse, UserItem, UserListResponse, UserProfileResponse
from apps.core.exceptions import NotFoundError
from apps.core.pagination import paginate_queryset


def get_user_profile(user: User) -> UserProfileResponse:
    # If employee relationship exists (linked via Employee model in master_data)
    employee_id = None
    name = user.username
    if hasattr(user, "employee_profile"):
        emp = user.employee_profile
        employee_id = emp.id
        name = emp.name

    roles = [r.name for r in user.roles.all()]

    return UserProfileResponse(
        id=user.id,
        username=user.username,
        name=name,
        employee_id=employee_id,
        roles=roles,
    )


def list_users(
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
) -> UserListResponse:
    qs = User.objects.prefetch_related("roles").order_by("-id")

    if search:
        qs = qs.filter(username__icontains=search)

    if role:
        qs = qs.filter(roles__name=role)

    if is_active is not None:
        qs = qs.filter(is_active=is_active)

    paginated = paginate_queryset(qs, page=page, page_size=page_size)

    items = [
        UserItem(
            id=u.id,
            username=u.username,
            is_active=u.is_active,
            is_staff=u.is_staff,
            roles=[r.name for r in u.roles.all()],
            created_at=u.created_at,
        )
        for u in paginated["items"]
    ]

    return UserListResponse(
        items=items,
        total=paginated["total"],
        page=paginated["page"],
        page_size=paginated["page_size"],
    )


def get_user_detail(user_id: int) -> UserItem:
    user = User.objects.prefetch_related("roles").filter(id=user_id).first()
    if not user:
        raise NotFoundError("Pengguna tidak ditemukan.")

    return UserItem(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
        roles=[r.name for r in user.roles.all()],
        created_at=user.created_at,
    )


def list_roles() -> RoleListResponse:
    roles = Role.objects.order_by("id")
    items = [RoleItem(id=r.id, name=r.name, description=r.description) for r in roles]
    return RoleListResponse(items=items)
