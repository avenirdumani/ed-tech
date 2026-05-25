import base64
import json
from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

T = TypeVar("T")


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    previous_cursor: str | None
    limit: int


def encode_cursor(created_at: datetime, id: UUID, direction: str = "fwd") -> str:
    payload = {"ts": created_at.isoformat(), "id": str(id), "dir": direction}
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()


def decode_cursor(cursor: str) -> tuple[datetime, UUID, str]:
    try:
        payload = json.loads(base64.urlsafe_b64decode(cursor.encode()))
        return datetime.fromisoformat(payload["ts"]), UUID(payload["id"]), payload.get("dir", "fwd")
    except Exception as exc:
        raise ValueError("Invalid pagination cursor") from exc


def paginate(
    session: Session,
    stmt: Any,
    entity_cls: Any,
    cursor: str | None,
    limit: int,
) -> tuple[list, str | None, str | None]:
    going_backward = False

    if cursor is not None:
        ts, id, direction = decode_cursor(cursor)
        going_backward = direction == "bwd"

        if going_backward:
            stmt = stmt.order_by(None).where(
                or_(
                    entity_cls.created_at < ts,
                    and_(entity_cls.created_at == ts, entity_cls.id < id),
                )
            ).order_by(entity_cls.created_at.desc(), entity_cls.id.desc())
        else:
            stmt = stmt.where(
                or_(
                    entity_cls.created_at > ts,
                    and_(entity_cls.created_at == ts, entity_cls.id > id),
                )
            )

    rows = session.scalars(stmt.limit(limit + 1)).all()
    has_more = len(rows) > limit
    items = list(rows[:limit])

    if going_backward:
        items.reverse()

    if not items:
        return items, None, None

    if going_backward:
        next_cursor = encode_cursor(items[-1].created_at, items[-1].id, "fwd")
        previous_cursor = encode_cursor(items[0].created_at, items[0].id, "bwd") if has_more else None
    else:
        next_cursor = encode_cursor(items[-1].created_at, items[-1].id, "fwd") if has_more else None
        previous_cursor = encode_cursor(items[0].created_at, items[0].id, "bwd") if cursor is not None else None

    return items, next_cursor, previous_cursor
