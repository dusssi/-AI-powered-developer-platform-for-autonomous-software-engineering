"""Add workspace repository registrations."""
from alembic import op
import sqlalchemy as sa

revision = "0002_repositories"
down_revision = "0001_users_workspaces"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "repositories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("clone_url", sa.String(length=500), nullable=False),
        sa.Column("default_branch", sa.String(length=120), nullable=True),
        sa.Column("connection_status", sa.String(length=40), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workspace_id", "clone_url", name="uq_repository_workspace_clone_url"
        ),
    )
    op.create_index("ix_repositories_workspace_id", "repositories", ["workspace_id"])


def downgrade():
    op.drop_index("ix_repositories_workspace_id", table_name="repositories")
    op.drop_table("repositories")
