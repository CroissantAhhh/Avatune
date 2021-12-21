"""empty message

Revision ID: 61e976a59832
Revises: 5fb809ac43c2
Create Date: 2021-12-21 09:46:16.026448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e976a59832'
down_revision = '5fb809ac43c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usertrackplays', sa.Column('last_played', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usertrackplays', 'last_played')
    # ### end Alembic commands ###
