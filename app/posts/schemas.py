from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.schemas import SoftDeleteSchema, TimestampSchema
from app.tags.schemas import TagResponse


class CreatePost(BaseModel):
    title: str = Field(min_length=5, max_length=255)
    content: str = Field(min_length=10)
    author_name: str = Field(min_length=2, max_length=100)
    author_email: EmailStr
    tags: list[UUID] = []


class UpdatePost(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=255)
    content: str | None = Field(None, min_length=10)
    author_name: str | None = Field(None, min_length=2, max_length=100)
    author_email: EmailStr | None = None
    tags: list[UUID] | None = None


class PostResponse(TimestampSchema, SoftDeleteSchema):
    entity_id: UUID
    title: str
    content: str
    author_name: str
    author_email: str
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)
