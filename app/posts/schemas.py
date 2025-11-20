from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.auth.schemas import UserResponse
from app.core.schemas import SoftDeleteSchema, TimestampSchema
from app.tags.schemas import TagResponse


class CreatePost(BaseModel):
    title: str = Field(min_length=5, max_length=255)
    content: str = Field(min_length=10)
    tags: list[UUID] = []


class UpdatePost(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=255)
    content: str | None = Field(None, min_length=10)
    tags: list[UUID] | None = None


class PostResponse(TimestampSchema, SoftDeleteSchema):
    entity_id: UUID
    title: str
    content: str
    user: UserResponse
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)
