from uuid import UUID
from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.core.models import (
    ApplicantProfile,
    ApplicantProgram,
    ChecklistItem,
    Program,
    TimelineEvent as TimelineEventModel,
)

from src.core.constants import ChecklistItemStatus, TimelineEventStatus
from src.repository import Repository
from src.core.exceptions import ConflictError, NotFoundError
from src.dtos.application import MissingRequirementOut, ApplicationReadinessOut


class ApplicationService:
    def __init__(self, session: Session) -> None:
        self.applications = Repository[ApplicantProgram](
            session,
            ApplicantProgram,
        )
        self.programs = Repository[Program](session, Program)
        self.profiles = Repository[ApplicantProfile](session, ApplicantProfile)
        self.checklist_items = Repository[ChecklistItem](
            session,
            ChecklistItem,
        )
        self.timeline_events = Repository[TimelineEventModel](
            session, TimelineEventModel
        )

    def get_preview(self, profile_id: UUID) -> list[ApplicantProgram]:
        applications, *_ = self.applications.list(
            None,
            3,
            ApplicantProgram.applicant_profile_id == profile_id,
        )
        return applications

    def list_applications(
        self,
        profile_id: UUID,
        cursor: str | None,
        limit: int,
    ) -> tuple[list[ApplicantProgram], str | None, str | None]:
        return self.applications.list(
            cursor,
            limit,
            ApplicantProgram.applicant_profile_id == profile_id,
        )

    def _check_can_create_application(
        self,
        profile_id: UUID,
        program_id: UUID,
    ) -> None:
        if self.profiles.get_by_id(profile_id) is None:
            raise NotFoundError(f"Profile {profile_id} not found")

        program = self.programs.get_by_id(program_id)
        if program is None:
            raise NotFoundError(f"Program {program_id} not found")

        if date.today() > program.application_deadline:
            raise ConflictError(
                f"Already past deadline for program {program_id}",
            )

        existing_application = self.applications.get_one(
            ApplicantProgram.applicant_profile_id == profile_id,
            ApplicantProgram.program_id == program_id,
        )
        if existing_application:
            raise ConflictError("Application already exists for this program")

    def create_application(self, profile_id: UUID, program_id: UUID):
        self._check_can_create_application(
            profile_id=profile_id,
            program_id=program_id,
        )

        new_application = ApplicantProgram(
            applicant_profile_id=profile_id, program_id=program_id
        )
        self.applications.save(new_application)

        deadline = new_application.program.application_deadline

        for requirement in new_application.program.requirements:
            due_date = deadline - timedelta(days=requirement.due_offset_days)
            new_checklist_item = ChecklistItem(
                status=ChecklistItemStatus.NOT_STARTED.value,
                due_date=due_date,
                applicant_program_id=new_application.id,
                program_requirement_id=requirement.id,
            )
            self.checklist_items.save(new_checklist_item)
            checklist_timeline_event = TimelineEventModel(
                applicant_program_id=new_application.id,
                checklist_item_id=new_checklist_item.id,
                title=requirement.title,
                date=due_date,
                status=TimelineEventStatus.UPCOMING,
            )
            self.timeline_events.save(checklist_timeline_event)
        self.checklist_items.flush()
        return new_application

    @staticmethod
    def _readiness_score(application: ApplicantProgram) -> float:
        required = [
            item
            for item in application.checklist_items
            if item.program_requirement.required
        ]
        completed = [
            item for item in required if item.status == ChecklistItemStatus.COMPLETE
        ]
        return round(len(completed) / len(required) * 100, 2) if required else 0.0

    @staticmethod
    def _missing_requirements(
        application: ApplicantProgram,
    ) -> list[MissingRequirementOut]:
        missing_requirements = []
        for item in application.checklist_items:
            if (
                not item.program_requirement.required
                or item.status == ChecklistItemStatus.COMPLETE
            ):
                continue
            missing_requirements.append(
                MissingRequirementOut(
                    requirement_id=item.program_requirement_id,
                    title=item.program_requirement.title,
                    type=item.program_requirement.type,
                    due_date=item.due_date,
                )
            )
        return missing_requirements

    @staticmethod
    def _next_milestones(
        application: ApplicantProgram,
    ) -> list[TimelineEventModel]:
        today = date.today()
        upcoming = [
            item.timeline_event
            for item in application.checklist_items
            if item.timeline_event is not None
            and item.timeline_event.status != TimelineEventStatus.COMPLETED
            and item.timeline_event.date >= today
        ]
        return sorted(upcoming, key=lambda e: e.date)

    def get_readiness(self, application: ApplicantProgram):
        return ApplicationReadinessOut(
            readiness_score=ApplicationService._readiness_score(application),
            missing_requirements=ApplicationService._missing_requirements(
                application,
            ),
            next_milestones=ApplicationService._next_milestones(application),
            checklist_items=application.checklist_items,
        )

    def get_application_timeline(self, application: ApplicantProgram):
        status_order = {
            TimelineEventStatus.COMPLETED: 0,
            TimelineEventStatus.OVERDUE: 1,
            TimelineEventStatus.DUE_SOON: 2,
            TimelineEventStatus.UPCOMING: 3,
        }
        events = [
            item.timeline_event
            for item in application.checklist_items
            if item.timeline_event is not None
        ]
        return sorted(events, key=lambda e: (status_order[e.status], e.date))

    def update_checklist_item_status(
        self,
        application: ApplicantProgram,
        checklist_item_id: UUID,
        status: ChecklistItemStatus,
    ) -> ChecklistItem:
        checklist_item = self.checklist_items.get_one(
            ChecklistItem.id == checklist_item_id,
            ChecklistItem.applicant_program_id == application.id,
        )
        if checklist_item is None:
            raise NotFoundError(f"Checklist item {checklist_item_id} not found")

        checklist_item.status = status

        timeline_event = checklist_item.timeline_event
        if timeline_event is not None:
            if status == ChecklistItemStatus.COMPLETE:
                timeline_event.status = TimelineEventStatus.COMPLETED
            else:
                today = date.today()
                if timeline_event.date < today:
                    timeline_event.status = TimelineEventStatus.OVERDUE
                elif (timeline_event.date - today).days <= 7:
                    timeline_event.status = TimelineEventStatus.DUE_SOON
                else:
                    timeline_event.status = TimelineEventStatus.UPCOMING

        self.checklist_items.save(checklist_item)
        return checklist_item
