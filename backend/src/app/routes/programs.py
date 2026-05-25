from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.app.dependencies import get_db, AuthenticateApplicant
from src.app.pagination import CursorPage, PaginationParams
from src.core.constants import DegreeType
from src.dtos.program import ProgramDetailOut, ProgramOut
from src.services.program import ProgramService

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get(
    "",
    response_model=CursorPage[ProgramOut],
    dependencies=[Depends(AuthenticateApplicant())],
)
def list_programs(
    pagination: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
    degree_type: Annotated[DegreeType | None, Query()] = None,
    name: Annotated[str | None, Query()] = None,
):
    items, next_cursor, previous_cursor = ProgramService(db).list_programs(
        degree_type, name, pagination.cursor, pagination.limit
    )
    return CursorPage(
        items=items,
        next_cursor=next_cursor,
        previous_cursor=previous_cursor,
        limit=pagination.limit,
    )


@router.get(
    "/{program_id}",
    response_model=ProgramDetailOut,
    dependencies=[Depends(AuthenticateApplicant())],
)
def get_program(program_id: UUID, db: Annotated[Session, Depends(get_db)]):
    return ProgramService(db).get_program(program_id)
