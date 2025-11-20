import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.schemas import TimestampSchema


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=12)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,12}$",
            v,
        ):
            raise ValueError("Password invalid: 8-12 chars, lower/upper/digit/special")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(TimestampSchema):
    entity_id: UUID
    name: str
    last_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
