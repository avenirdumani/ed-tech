from __future__ import annotations
from datetime import date
from uuid import UUID

from sqlalchemy import (
    Boolean,
    String,
    Float,
    SmallInteger,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.mixins import Base, EntityMixin
from src.core import constants


class User(Base, EntityMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[constants.UserRole] = mapped_column(
        String,
        index=True,
        nullable=False,
    )

    applicant_profile: Mapped[ApplicantProfile | None] = relationship(
        "ApplicantProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )


class ApplicantProfile(Base, EntityMixin):
    __tablename__ = "applicant_profile"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    family_name: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
    )
    gpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_term: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    user: Mapped[User] = relationship(
        "User",
        back_populates="applicant_profile",
    )

    @property
    def email(self) -> str:
        return self.user.email

    applications: Mapped[list[ApplicantProgram]] = relationship(
        "ApplicantProgram",
        back_populates="applicant_profile",
        cascade="all, delete-orphan",
        lazy=True,
    )


class Program(Base, EntityMixin):
    __tablename__ = "program"

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    degree_type: Mapped[constants.DegreeType] = mapped_column(
        String, index=True, nullable=False
    )
    application_deadline: Mapped[date] = mapped_column(
        Date,
        index=True,
        nullable=True,
    )

    requirements: Mapped[list[ProgramRequirement]] = relationship(
        "ProgramRequirement",
        back_populates="program",
        cascade="all, delete-orphan",
    )


class ProgramRequirement(Base, EntityMixin):
    __tablename__ = "program_requirement"

    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    type: Mapped[constants.RequirementType] = mapped_column(
        String,
        index=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    evidence_type: Mapped[constants.EvidenceType] = mapped_column(
        String,
        nullable=False,
    )
    due_offset_days: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
    )
    required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    program_id: Mapped[UUID] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"),
        index=True,
    )
    program: Mapped[Program] = relationship(
        "Program",
        back_populates="requirements",
    )


class ApplicantProgram(Base, EntityMixin):
    __tablename__ = "applicant_program"

    applicant_profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("applicant_profile.id", ondelete="CASCADE"), index=True
    )
    applicant_profile: Mapped[ApplicantProfile] = relationship(
        "ApplicantProfile",
        back_populates="applications",
        lazy=True,
    )

    program_id: Mapped[UUID] = mapped_column(
        ForeignKey("program.id"),
        index=True,
    )
    program: Mapped[Program] = relationship("Program", lazy=True)

    checklist_items: Mapped[list[ChecklistItem]] = relationship(
        "ChecklistItem",
        back_populates="applicant_program",
        cascade="all, delete-orphan",
        lazy=True,
    )

    @property
    def readiness_score(self) -> float:
        required = [
            item for item in self.checklist_items if item.program_requirement.required
        ]
        completed = [
            item
            for item in required
            if item.status == constants.ChecklistItemStatus.COMPLETE
        ]
        return round(len(completed) / len(required) * 100, 2) if required else 0

    @property
    def next_milestone(self) -> TimelineEvent | None:
        today = date.today()
        upcoming = [
            item.timeline_event
            for item in self.checklist_items
            if item.timeline_event is not None
            and item.timeline_event.status != constants.TimelineEventStatus.COMPLETED
            and item.timeline_event.date >= today
        ]
        return min(upcoming, key=lambda e: e.date) if upcoming else None


class ChecklistItem(Base, EntityMixin):
    __tablename__ = "checklist_item"

    status: Mapped[constants.ChecklistItemStatus] = mapped_column(
        String, index=True, nullable=False
    )
    due_date: Mapped[date | None] = mapped_column(
        Date,
        index=True,
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    applicant_program_id: Mapped[UUID] = mapped_column(
        ForeignKey("applicant_program.id", ondelete="CASCADE"),
        index=True,
    )
    applicant_program: Mapped[ApplicantProgram] = relationship(
        "ApplicantProgram",
        back_populates="checklist_items",
        lazy=True,
    )

    program_requirement_id: Mapped[UUID] = mapped_column(
        ForeignKey("program_requirement.id", ondelete="RESTRICT"),
        index=True,
    )
    program_requirement: Mapped[ProgramRequirement] = relationship(
        "ProgramRequirement",
        lazy=True,
    )

    @property
    def requirement_id(self) -> UUID:
        return self.program_requirement_id

    @property
    def requirement_title(self) -> str:
        return self.program_requirement.title

    @property
    def requirement_type(self) -> constants.RequirementType:
        return self.program_requirement.type

    @property
    def required(self) -> bool:
        return self.program_requirement.required

    timeline_event: Mapped[TimelineEvent | None] = relationship(
        "TimelineEvent",
        back_populates="checklist_item",
        cascade="all, delete-orphan",
        foreign_keys="[TimelineEvent.checklist_item_id]",
        uselist=False,
    )


class TimelineEvent(Base, EntityMixin):
    __tablename__ = "timeline_event"

    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[constants.TimelineEventStatus] = mapped_column(
        String,
        index=True,
        nullable=False,
    )

    applicant_program_id: Mapped[UUID] = mapped_column(
        ForeignKey("applicant_program.id", ondelete="CASCADE"),
        index=True,
    )
    checklist_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("checklist_item.id", ondelete="CASCADE"),
        index=True,
    )
    checklist_item: Mapped[ChecklistItem] = relationship(
        "ChecklistItem",
        back_populates="timeline_event",
        lazy=True,
    )
