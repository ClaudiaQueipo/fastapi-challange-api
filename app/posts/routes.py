from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session
from app.posts.schemas import CreatePost, PostResponse, UpdatePost
from app.posts.services import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(
    post_data: CreatePost,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostResponse:
    service = PostService(session)
    post = await service.create_post(post_data)
    return PostResponse.model_validate(post)


@router.get("", response_model=list[PostResponse], status_code=200)
async def list_posts(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    only_deleted: Annotated[bool, Query()] = False,
) -> list[PostResponse]:
    service = PostService(session)
    posts = await service.list_posts(page, size, only_deleted)
    return [PostResponse.model_validate(post) for post in posts]


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
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostResponse:
    service = PostService(session)
    post = await service.update_post(entity_id, update_data)
    return PostResponse.model_validate(post)


@router.delete("/{entity_id}", status_code=204)
async def delete_post(
    entity_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    service = PostService(session)
    await service.delete_post(entity_id)
