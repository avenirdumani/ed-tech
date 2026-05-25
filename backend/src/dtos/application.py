from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.dtos.program import ProgramOut

from src.core.constants import (
    ChecklistItemStatus,
    RequirementType,
    TimelineEventStatus,
)


class ChecklistItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    requirement_id: UUID
    requirement_title: str
    requirement_type: RequirementType
    required: bool
    status: ChecklistItemStatus
    due_date: date | None
    notes: str | None


class MissingRequirementOut(BaseModel):
    requirement_id: UUID
    title: str
    type: RequirementType
    due_date: date | None


class NextMilestoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    due_date: date = Field(alias="date")
    status: TimelineEventStatus


class ApplicationReadinessOut(BaseModel):
    readiness_score: float
    missing_requirements: list[MissingRequirementOut]
    next_milestones: list[NextMilestoneOut]
    checklist_items: list[ChecklistItemOut]


class TimelineEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    date: date
    status: TimelineEventStatus
    checklist_item: ChecklistItemOut


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    program: ProgramOut
    readiness_score: float
    next_milestone: NextMilestoneOut | None


class ApplicationDetailOut(ApplicationOut):
    checklist_items: list[ChecklistItemOut]


class ApplicationCreate(BaseModel):
    program_id: UUID


class ChecklistItemStatusUpdate(BaseModel):
    status: ChecklistItemStatus
