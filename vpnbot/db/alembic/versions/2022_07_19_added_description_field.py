"""Added_description_field

Revision ID: e7eb59f75785
Revises: 59e81535b967
Create Date: 2022-07-19 12:39:36.223971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7eb59f75785'
down_revision = '59e81535b967'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'description')
    # ### end Alembic commands ###
