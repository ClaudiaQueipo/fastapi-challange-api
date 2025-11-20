from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.schemas import SoftDeleteSchema, TimestampSchema


class CreateTag(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class UpdateTag(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)


class TagResponse(TimestampSchema, SoftDeleteSchema):
    entity_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
