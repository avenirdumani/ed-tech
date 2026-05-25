from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.dtos.user import Token, UserAuthenticate
from src.services.user import UserService

router = APIRouter(tags=["user"])


@router.post("/login", response_model=Token)
def login(
    authentication_data: UserAuthenticate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    return UserService(session=db).authenticate_user(
        authentication_data=authentication_data
    )
