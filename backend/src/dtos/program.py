from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.core.constants import DegreeType, EvidenceType, RequirementType


class RequirementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    type: RequirementType
    description: str
    evidence_type: EvidenceType
    due_offset_days: int
    required: bool


class ProgramOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    degree_type: DegreeType
    application_deadline: date | None


class ProgramDetailOut(ProgramOut):
    requirements: list[RequirementOut]
