from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetailItem(BaseModel):
    field: str | None = None
    message: str


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: List[ErrorDetailItem] | None = None
    request_id: str


class SuccessMessageResponse(BaseModel):
    message: str


class GenericPaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
