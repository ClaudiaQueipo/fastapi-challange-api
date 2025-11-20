from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.core.mixins import SoftDeleteMixin, TimestampMixin
from app.posts.models import post_tags

if TYPE_CHECKING:
    from app.auth.models import User
    from app.posts.models import Post


class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"

    entity_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.entity_id"), nullable=False
    )
    user: Mapped[User] = relationship("User")
    posts: Mapped[list[Post]] = relationship(
        "Post", secondary=post_tags, back_populates="tags"
    )
