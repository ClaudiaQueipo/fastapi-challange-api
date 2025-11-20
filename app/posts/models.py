from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.core.mixins import SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from app.tags.models import Tag

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", UUID(as_uuid=True), ForeignKey("posts.entity_id")),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.entity_id")),
)


class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    entity_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    author_email: Mapped[str] = mapped_column(String(255), nullable=False)
    tags: Mapped[list[Tag]] = relationship(
        "Tag", secondary=post_tags, back_populates="posts"
    )
