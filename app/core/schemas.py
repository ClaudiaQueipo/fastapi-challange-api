from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SoftDeleteSchema(BaseModel):
    is_deleted: bool
    deleted_at: datetime | None = None


class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
