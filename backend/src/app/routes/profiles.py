from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.app.dependencies import get_db, AuthenticateApplicant
from src.dtos.profile import ProfileCreate, ProfileOut, ProfileUpdate
from src.services.profile import ProfileService
from src.core.models import ApplicantProfile

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post(
    "",
    response_model=ProfileOut,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    body: ProfileCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return ProfileService(db).create_profile(body)


@router.get("", response_model=ProfileOut)
def get_profile(
    applicant_profile: Annotated[
        ApplicantProfile,
        Depends(AuthenticateApplicant()),
    ],
):
    return applicant_profile


@router.patch("", response_model=ProfileOut)
def update_profile(
    applicant_profile: Annotated[
        ApplicantProfile,
        Depends(AuthenticateApplicant()),
    ],
    body: ProfileUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    return ProfileService(db).update_profile(applicant_profile, body)
