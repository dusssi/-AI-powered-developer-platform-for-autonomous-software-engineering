"""Add GitHub App installation records and one-time setup state."""
from alembic import op
import sqlalchemy as sa

revision = "0003_github_installations"
down_revision = "0002_repositories"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "github_installations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("installation_id", sa.BigInteger(), nullable=False),
        sa.Column("account_login", sa.String(length=200), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("installation_id", name="uq_github_installation_id"),
    )
    op.create_index("ix_github_installations_workspace_id", "github_installations", ["workspace_id"])
    op.create_table(
        "github_install_states",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("state_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("state_hash"),
    )
    op.create_index("ix_github_install_states_workspace_id", "github_install_states", ["workspace_id"])
    op.create_index("ix_github_install_states_state_hash", "github_install_states", ["state_hash"])


def downgrade():
    op.drop_index("ix_github_install_states_state_hash", table_name="github_install_states")
    op.drop_index("ix_github_install_states_workspace_id", table_name="github_install_states")
    op.drop_table("github_install_states")
    op.drop_index("ix_github_installations_workspace_id", table_name="github_installations")
    op.drop_table("github_installations")
