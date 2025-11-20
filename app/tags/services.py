from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mixins import CRUDMixin
from app.tags.models import Tag
from app.tags.schemas import CreateTag, UpdateTag


class TagService(CRUDMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_tag(self, tag_data: CreateTag, user_id: UUID) -> Tag:
        tag = Tag(**tag_data.model_dump(), user_id=user_id)
        return await self.create(tag)

    async def get_tag(self, entity_id: UUID) -> Tag:
        return await self.get_by_id(Tag, entity_id)

    async def update_tag(self, entity_id: UUID, update_data: UpdateTag) -> Tag:
        tag = await self.get_tag(entity_id)
        update_dict = update_data.model_dump(exclude_unset=True)
        return await self.update(tag, update_dict)

    async def delete_tag(self, entity_id: UUID) -> None:
        tag = await self.get_tag(entity_id)
        await self.delete(tag)

    async def list_tags(
        self, page: int = 1, size: int = 10, only_deleted: bool = False
    ) -> tuple[list[Tag], int]:
        tags = await self.list_paginated(Tag, page, size, only_deleted)
        count_stmt = select(func.count(Tag.entity_id))
        if only_deleted:
            count_stmt = count_stmt.where(Tag.is_deleted)
        else:
            count_stmt = count_stmt.where(Tag.is_deleted == False)  # noqa: E712
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar()
        return tags, total
