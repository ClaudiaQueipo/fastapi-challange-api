from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session
from app.tags.schemas import CreateTag, TagResponse, UpdateTag
from app.tags.services import TagService

router = APIRouter(prefix="/tags", tags=["tags"])


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@router.post("", response_model=TagResponse, status_code=201)
async def create_tag(
    tag_data: CreateTag,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagResponse:
    service = TagService(session)
    tag = await service.create_tag(tag_data)
    return TagResponse.model_validate(tag)


@router.get("", response_model=list[TagResponse], status_code=200)
async def list_tags(
    session: Annotated[AsyncSession, Depends(get_session)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    only_deleted: Annotated[bool, Query()] = False,
) -> list[TagResponse]:
    service = TagService(session)
    tags = await service.list_tags(page, size, only_deleted)
    return [TagResponse.model_validate(tag) for tag in tags]


@router.get("/{entity_id}", response_model=TagResponse, status_code=200)
async def get_tag(
    entity_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagResponse:
    service = TagService(session)
    tag = await service.get_tag(entity_id)
    return TagResponse.model_validate(tag)


@router.put("/{entity_id}", response_model=TagResponse, status_code=200)
async def update_tag(
    entity_id: UUID,
    update_data: UpdateTag,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagResponse:
    service = TagService(session)
    tag = await service.update_tag(entity_id, update_data)
    return TagResponse.model_validate(tag)


@router.delete("/{entity_id}", status_code=204)
async def delete_tag(
    entity_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    service = TagService(session)
    await service.delete_tag(entity_id)
