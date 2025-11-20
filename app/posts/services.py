from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.models import User
from app.core.mixins import CRUDMixin
from app.posts.models import Post
from app.posts.schemas import CreatePost, UpdatePost
from app.tags.models import Tag


class PostService(CRUDMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_post(self, post_data: CreatePost, user_id: UUID) -> Post:
        # Get current user
        result = await self.session.execute(
            select(User).where(User.entity_id == user_id)
        )
        current_user = result.scalar_one()

        post = Post(**post_data.model_dump(exclude={"tags"}), user_id=user_id)
        post = await self.create(post)
        if post_data.tags:
            result = await self.session.execute(
                select(Tag)
                .where(Tag.entity_id.in_(post_data.tags))
                .where(Tag.is_deleted == False)  # noqa: E712
            )
            post.tags = result.scalars().all()
        await self.session.commit()
        await self.session.refresh(post)

        post.user = current_user
        return post

    async def get_post(self, entity_id: UUID) -> Post:
        stmt = (
            select(Post)
            .options(selectinload(Post.tags), selectinload(Post.user))
            .where(Post.entity_id == entity_id)
        )
        result = await self.session.execute(stmt)
        post = result.scalar_one_or_none()
        if not post or post.is_deleted:
            from app.core.exceptions import ResourceNotFoundError

            raise ResourceNotFoundError("Resource not found")
        post.tags = [tag for tag in post.tags if not tag.is_deleted]
        return post

    async def update_post(self, entity_id: UUID, update_data: UpdatePost) -> Post:
        post = await self.get_post(entity_id)
        update_dict = update_data.model_dump(exclude_unset=True, exclude={"tags"})
        post = await self.update(post, update_dict)
        if update_data.tags is not None:
            result = await self.session.execute(
                select(Tag)
                .where(Tag.entity_id.in_(update_data.tags))
                .where(Tag.is_deleted == False)  # noqa: E712
            )
            post.tags = result.scalars().all()
            await self.session.commit()
            await self.session.refresh(post)
        return post

    async def delete_post(self, entity_id: UUID) -> None:
        post = await self.get_post(entity_id)
        await self.delete(post)

    async def list_posts(
        self, page: int = 1, size: int = 10, only_deleted: bool = False
    ) -> tuple[list[Post], int]:
        stmt = select(Post).options(selectinload(Post.tags), selectinload(Post.user))
        if only_deleted:
            stmt = stmt.where(Post.is_deleted)
        else:
            stmt = stmt.where(Post.is_deleted == False)  # noqa: E712
        paginated_stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(paginated_stmt)
        posts = result.scalars().all()
        for post in posts:
            post.tags = [tag for tag in post.tags if not tag.is_deleted]

        count_stmt = select(func.count(Post.entity_id))
        if only_deleted:
            count_stmt = count_stmt.where(Post.is_deleted)
        else:
            count_stmt = count_stmt.where(Post.is_deleted == False)  # noqa: E712
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar()

        return posts, total
