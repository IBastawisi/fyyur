"""empty message

Revision ID: 24519d69bdc3
Revises: 83de1e6d43e5
Create Date: 2020-07-17 09:34:31.209509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24519d69bdc3'
down_revision = '83de1e6d43e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genres')
    # ### end Alembic commands ###
