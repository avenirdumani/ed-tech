from sqlalchemy.orm import Session

from src.dtos.user import UserAuthenticate, Token, UserCreate
from src.repository import Repository
from src.core.models import User
from src.core.utils import (
    validate_password,
    create_access_token,
    hash_password,
)
from src.core.exceptions import CredentialError


class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = Repository(session, User)

    def create_user(self, data: UserCreate) -> User:
        existing_user = self.users.get_one(User.email == data.email)
        if existing_user:
            raise Exception()
        hashed_password = hash_password(plain_password=data.password)
        new_user = User(
            email=data.email,
            password=hashed_password,
            role=data.role,
        )
        self.users.save(new_user)
        return new_user

    def authenticate_user(
        self,
        authentication_data: UserAuthenticate,
    ) -> Token:
        found_user = self.users.get_one(
            User.email == authentication_data.email,
        )
        if not found_user:
            raise CredentialError()
        if not validate_password(
            plain_password=authentication_data.password,
            hashed_password=found_user.password,
        ):
            raise CredentialError()
        token = create_access_token(data={"sub": found_user.email})
        return Token(access_token=token)
