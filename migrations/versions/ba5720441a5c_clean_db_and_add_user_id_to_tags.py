"""Clean DB and add user_id to tags

Revision ID: ba5720441a5c
Revises: de9dc0d0bc49
Create Date: 2025-11-20 11:09:37.454745

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ba5720441a5c"
down_revision: str | Sequence[str] | None = "de9dc0d0bc49"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Clean posts and tags
    op.execute("DELETE FROM post_tags")
    op.execute("DELETE FROM posts")
    op.execute("DELETE FROM tags")
    # Add user_id to tags
    op.add_column("tags", sa.Column("user_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        "fk_tags_user_id",
        "tags",
        "users",
        ["user_id"],
        ["entity_id"],
    )
    # Make user_id not null in posts (already added in previous migration)
    op.alter_column("posts", "user_id", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove user_id from tags
    op.drop_constraint("fk_tags_user_id", "tags", type_="foreignkey")
    op.drop_column("tags", "user_id")
    # Make user_id nullable in posts
    op.alter_column("posts", "user_id", nullable=True)
