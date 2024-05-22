"""added email_token for user

Revision ID: fd11044eb898
Revises: d60e529d9d80
Create Date: 2023-05-27 21:46:33.806734

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fd11044eb898"
down_revision = "d60e529d9d80"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("email_token", sa.Uuid(), nullable=False))
    op.create_unique_constraint("users_email_token", "users", ["email_token"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("users_email_token", "users", type_="unique")
    op.drop_column("users", "email_token")
    # ### end Alembic commands ###
