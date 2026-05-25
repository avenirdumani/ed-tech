from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.core.models import ApplicantProfile, User
from src.repository import Repository
from src.dtos.profile import ProfileCreate, ProfileUpdate
from src.dtos.user import UserCreate
from src.services.user import UserService
from src.core.constants import UserRole


class ProfileService:
    def __init__(self, session: Session) -> None:
        self.profiles = Repository(session, ApplicantProfile)
        self.users = Repository(session, User)
        self.users_service = UserService(session=session)

    def create_profile(self, data: ProfileCreate) -> ApplicantProfile:
        user = self.users_service.create_user(
            data=UserCreate(
                email=data.email,
                password=data.password,
                role=UserRole.APPLICANT,
            )
        )
        profile = ApplicantProfile(
            name=data.name,
            family_name=data.family_name,
            gpa=data.gpa,
            target_term=data.target_term,
            user_id=user.id,
        )
        self.profiles.save(profile)
        return profile

    def update_profile(
        self, profile: ApplicantProfile, data: ProfileUpdate
    ) -> ApplicantProfile:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(profile, field, value)
        profile.updated_at = datetime.now(tz=timezone.utc)

        self.profiles.flush()
        return profile
