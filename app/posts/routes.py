from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.db import async_session
from app.core.exceptions import PermissionDeniedError
from app.core.schemas import PaginatedResponse
from app.posts.models import Post
from app.posts.schemas import CreatePost, PostResponse, UpdatePost
from app.posts.services import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(
    post_data: CreatePost,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostResponse:
    service = PostService(session)
    post = await service.create_post(post_data, current_user.entity_id)
    stmt = (
        select(Post)
        .options(selectinload(Post.user), selectinload(Post.tags))
        .where(Post.entity_id == post.entity_id)
    )
    result = await session.execute(stmt)
    post = result.scalar_one()
    return PostResponse.model_validate(post)


@router.get("", response_model=PaginatedResponse[PostResponse], status_code=200)
async def list_posts(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    only_deleted: Annotated[bool, Query()] = False,
) -> PaginatedResponse[PostResponse]:
    service = PostService(session)
    posts, total = await service.list_posts(page, size, only_deleted)
    return PaginatedResponse(
        items=[PostResponse.model_validate(post) for post in posts], total=total
    )


@router.get("/{entity_id}", response_model=PostResponse, status_code=200)
async def get_post(
    entity_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostResponse:
    service = PostService(session)
    post = await service.get_post(entity_id)
    return PostResponse.model_validate(post)


@router.put("/{entity_id}", response_model=PostResponse, status_code=200)
async def update_post(
    entity_id: UUID,
    update_data: UpdatePost,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostResponse:
    service = PostService(session)
    post = await service.get_post(entity_id)
    if post.user_id != current_user.entity_id:
        raise PermissionDeniedError("Not authorized")
    post = await service.update_post(entity_id, update_data)
    return PostResponse.model_validate(post)


@router.delete("/{entity_id}", status_code=204)
async def delete_post(
    entity_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    service = PostService(session)
    post = await service.get_post(entity_id)
    if post.user_id != current_user.entity_id:
        raise PermissionDeniedError("Not authorized")
    await service.delete_post(entity_id)
