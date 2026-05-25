from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileCreate(BaseModel):
    name: str
    family_name: str
    email: str
    password: str
    gpa: float = Field(default=0, ge=0.0, le=4.0)
    target_term: str

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()


class ProfileUpdate(BaseModel):
    name: str | None = None
    family_name: str | None = None
    gpa: float | None = Field(default=None, ge=0.0, le=4.0)
    target_term: str | None = None


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attibutes=True)

    id: UUID
    name: str
    family_name: str
    email: str
    gpa: float
    target_term: str
