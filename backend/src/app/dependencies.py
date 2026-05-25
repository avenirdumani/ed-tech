from collections.abc import Generator
from typing import Annotated
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from src.core.db import LocalSessionMaker
from src.core.models import User, ApplicantProfile, ApplicantProgram
from src.core.settings import app_settings
from src.repository import Repository


def get_db() -> Generator[Session, None, None]:
    db = LocalSessionMaker()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthenticateApplicant:
    def __call__(
        self,
        db: Annotated[Session, Depends(get_db)],
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> None:
        users = Repository[User](session=db, model_cls=User)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                app_settings.secret_key,
                algorithms=["HS256"],
            )
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = users.get_one(User.email == email)
        if user is None:
            raise credentials_exception
        return user.applicant_profile


class GetApplication:
    def __call__(
        self,
        db: Annotated[Session, Depends(get_db)],
        applicant_profile: Annotated[
            ApplicantProfile, Depends(AuthenticateApplicant())
        ],
        application_id: Annotated[UUID, Path()],
    ) -> None:
        application_programs = Repository[ApplicantProgram](
            session=db, model_cls=ApplicantProgram
        )
        found_application = application_programs.get_one(
            ApplicantProgram.applicant_profile_id == applicant_profile.id
        )
        if not found_application:
            raise Exception()
        return found_application
