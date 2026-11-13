from typing import Any, Dict

from django.db.models import QuerySet


def paginate_queryset(queryset: QuerySet, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20
    if page_size > 100:
        page_size = 100

    total = queryset.count()
    offset = (page - 1) * page_size
    items = list(queryset[offset : offset + page_size])

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }
