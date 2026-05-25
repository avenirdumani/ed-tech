from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.db.mixins import Base
from src.core.pagination import paginate

T = TypeVar("T", bound=Base)


class Repository(Generic[T]):
    def __init__(self, session: Session, model_cls: type[T]) -> None:
        self.session = session
        self.model_cls = model_cls

    def get_by_id(self, id: UUID) -> T | None:
        return self.session.get(self.model_cls, id)

    def get_one(self, *where_clauses: Any) -> T | None:
        stmt = select(self.model_cls).where(*where_clauses)
        return self.session.scalars(stmt).first()

    def list(
        self,
        cursor: str | None,
        limit: int,
        *where_clauses: Any,
    ) -> tuple[list[T], str | None, str | None]:
        stmt = select(self.model_cls).order_by(
            self.model_cls.created_at, self.model_cls.id
        )
        if where_clauses:
            stmt = stmt.where(*where_clauses)
        return paginate(self.session, stmt, self.model_cls, cursor, limit)

    def save(self, obj: T) -> None:
        self.session.add(obj)
        self.session.flush()

    def flush(self) -> None:
        self.session.flush()
