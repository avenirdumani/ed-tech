from fastapi import Query

from src.core.pagination import CursorPage  # re-exported for router convenience

__all__ = ["CursorPage", "PaginationParams"]


class PaginationParams:
    def __init__(
        self,
        cursor: str | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
    ):
        self.cursor = cursor
        self.limit = limit
