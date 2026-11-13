from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900


class LogoutRequest(BaseModel):
    refresh_token: str


class UserProfileResponse(BaseModel):
    id: int
    username: str
    name: str
    employee_id: Optional[int] = None
    roles: List[str]


class UserItem(BaseModel):
    id: int
    username: str
    is_active: bool
    is_staff: bool
    roles: List[str]
    created_at: datetime


class UserListResponse(BaseModel):
    items: List[UserItem]
    total: int
    page: int
    page_size: int


class UserCreateRequest(BaseModel):
    username: str
    password: str
    roles: List[str]
    is_active: bool = True


class UserUpdateRequest(BaseModel):
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None


class RoleItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class RoleListResponse(BaseModel):
    items: List[RoleItem]
