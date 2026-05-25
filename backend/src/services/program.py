from uuid import UUID

from sqlalchemy.orm import Session

from src.core.constants import DegreeType
from src.core.exceptions import NotFoundError
from src.core.models import Program
from src.repository import Repository


class ProgramService:
    def __init__(self, session: Session) -> None:
        self.repo = Repository(session, Program)

    def list_programs(
        self,
        degree_type: DegreeType | None,
        name: str | None,
        cursor: str | None,
        limit: int,
    ) -> tuple[list[Program], str | None, str | None]:
        filters = []
        if degree_type is not None:
            filters.append(Program.degree_type == degree_type)
        if name is not None:
            filters.append(Program.name.ilike(f"%{name}%"))

        return self.repo.list(cursor, limit, *filters)

    def get_program(self, program_id: UUID) -> Program:
        program = self.repo.get_by_id(program_id)
        if program is None:
            raise NotFoundError(f"Program {program_id} not found")
        return program
