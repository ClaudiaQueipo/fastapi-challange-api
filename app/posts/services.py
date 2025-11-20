from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mixins import CRUDMixin
from app.posts.models import Post
from app.posts.schemas import CreatePost, UpdatePost


class PostService(CRUDMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_post(self, post_data: CreatePost) -> Post:
        post = Post(**post_data.model_dump())
        return await self.create(post)

    async def get_post(self, entity_id: UUID) -> Post:
        return await self.get_by_id(Post, entity_id)

    async def update_post(self, entity_id: UUID, update_data: UpdatePost) -> Post:
        post = await self.get_post(entity_id)
        update_dict = update_data.model_dump(exclude_unset=True)
        return await self.update(post, update_dict)

    async def delete_post(self, entity_id: UUID) -> None:
        post = await self.get_post(entity_id)
        await self.delete(post)

    async def list_posts(
        self, page: int = 1, size: int = 10, only_deleted: bool = False
    ) -> list[Post]:
        return await self.list_paginated(Post, page, size, only_deleted)
