from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.core.exceptions import ResourceNotFoundError


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()


class CRUDMixin:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: Any) -> Any:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, model: type[Any], entity_id: Any) -> Any:
        result = await self.session.get(model, entity_id)
        if not result or result.is_deleted:
            raise ResourceNotFoundError("Resource not found")
        return result

    async def update(self, obj: Any, update_data: dict[str, Any]) -> Any:
        for key, value in update_data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: Any) -> None:
        obj.soft_delete()
        await self.session.commit()

    async def list_paginated(
        self,
        model: type[Any],
        page: int = 1,
        size: int = 10,
        only_deleted: bool = False,
    ) -> list[Any]:
        stmt = select(model)
        if only_deleted:
            stmt = stmt.where(model.is_deleted)
        else:
            stmt = stmt.where(model.is_deleted == False)  # noqa: E712
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return result.scalars().all()
