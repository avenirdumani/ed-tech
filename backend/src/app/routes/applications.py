from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.app.dependencies import get_db, AuthenticateApplicant, GetApplication
from src.app.pagination import CursorPage, PaginationParams
from src.dtos.application import (
    ApplicationOut,
    ApplicationDetailOut,
    ApplicationCreate,
    ApplicationReadinessOut,
    TimelineEventOut,
    ChecklistItemOut,
    ChecklistItemStatusUpdate,
)
from src.services.application import ApplicationService
from src.core.models import ApplicantProfile, ApplicantProgram

router = APIRouter(tags=["applications"])


@router.get(
    "/applications",
    response_model=CursorPage[ApplicationOut],
)
def list_applications(
    applicant_profile: Annotated[
        ApplicantProfile,
        Depends(AuthenticateApplicant()),
    ],
    pagination: Annotated[PaginationParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    items, next_cursor, previous_cursor = ApplicationService(db).list_applications(
        applicant_profile.id, pagination.cursor, pagination.limit
    )
    return CursorPage(
        items=items,
        next_cursor=next_cursor,
        previous_cursor=previous_cursor,
        limit=pagination.limit,
    )


@router.post("/applications", response_model=ApplicationOut)
def create_application(
    applicant_profile: Annotated[
        ApplicantProfile,
        Depends(AuthenticateApplicant()),
    ],
    db: Annotated[Session, Depends(get_db)],
    data: ApplicationCreate,
):
    service = ApplicationService(session=db)
    return service.create_application(
        profile_id=applicant_profile.id, program_id=data.program_id
    )


@router.get("/applications/preview", response_model=list[ApplicationOut])
def get_applications_preview(
    applicant_profile: Annotated[
        ApplicantProfile,
        Depends(AuthenticateApplicant()),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    service = ApplicationService(session=db)
    return service.get_preview(profile_id=applicant_profile.id)


@router.get(
    "/applications/{application_id}",
    response_model=ApplicationDetailOut,
)
def get_application(
    application: Annotated[ApplicantProgram, Depends(GetApplication())],
):
    return application


@router.get(
    "/applications/{application_id}/readiness",
    response_model=ApplicationReadinessOut,
)
def get_application_readiness(
    application: Annotated[ApplicantProgram, Depends(GetApplication())],
    db: Annotated[Session, Depends(get_db)],
):
    service = ApplicationService(session=db)
    return service.get_readiness(application=application)


#
#
@router.get(
    "/applications/{application_id}/timeline",
    response_model=list[TimelineEventOut],
)
def get_application_timeline(
    application: Annotated[ApplicantProgram, Depends(GetApplication())],
    db: Annotated[Session, Depends(get_db)],
):
    service = ApplicationService(session=db)
    return service.get_application_timeline(application=application)


@router.patch(
    "/applications/{application_id}/checklist/{checklist_id}",
    response_model=ChecklistItemOut,
)
def update_checklist_item_status(
    application: Annotated[ApplicantProgram, Depends(GetApplication())],
    checklist_id: Annotated[UUID, Path()],
    db: Annotated[Session, Depends(get_db)],
    data: ChecklistItemStatusUpdate,
):
    service = ApplicationService(session=db)
    return service.update_checklist_item_status(
        application=application,
        checklist_item_id=checklist_id,
        status=data.status,
    )
