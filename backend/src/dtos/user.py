from pydantic import BaseModel, Field

from src.core.constants import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole


class UserAuthenticate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")
