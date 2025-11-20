"""Add User model and update Post model for authentication

Revision ID: de9dc0d0bc49
Revises: afac8ee83228
Create Date: 2025-11-20 10:29:07.642877

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "de9dc0d0bc49"
down_revision: str | Sequence[str] | None = "afac8ee83228"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        "users",
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("entity_id"),
        sa.UniqueConstraint("email"),
    )
    # Add user_id column to posts
    op.add_column("posts", sa.Column("user_id", sa.UUID(), nullable=True))
    # Create foreign key
    op.create_foreign_key(
        "fk_posts_user_id",
        "posts",
        "users",
        ["user_id"],
        ["entity_id"],
    )
    # Remove author_name and author_email columns
    op.drop_column("posts", "author_name")
    op.drop_column("posts", "author_email")


def downgrade() -> None:
    """Downgrade schema."""
    # Add back author_name and author_email columns
    op.add_column(
        "posts", sa.Column("author_name", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "posts", sa.Column("author_email", sa.String(length=255), nullable=True)
    )
    # Drop foreign key
    op.drop_constraint("fk_posts_user_id", "posts", type_="foreignkey")
    # Drop user_id column
    op.drop_column("posts", "user_id")
    # Drop users table
    op.drop_table("users")
