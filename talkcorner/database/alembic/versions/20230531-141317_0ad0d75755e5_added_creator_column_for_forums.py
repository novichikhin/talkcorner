"""added creator column for forums

Revision ID: 0ad0d75755e5
Revises: fd11044eb898
Create Date: 2023-05-31 14:13:17.252992

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0ad0d75755e5"
down_revision = "fd11044eb898"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("forums", sa.Column("creator_id", sa.Uuid(), nullable=False))
    op.create_foreign_key(
        "forums_creator_id_fkey", "forums", "users", ["creator_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("forums_creator_id_fkey", "forums", type_="foreignkey")
    op.drop_column("forums", "creator_id")
    # ### end Alembic commands ###
