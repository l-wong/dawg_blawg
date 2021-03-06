"""empty message

Revision ID: e60846c31bff
Revises: 94409075500d
Create Date: 2020-07-01 23:50:22.592811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e60846c31bff'
down_revision = '94409075500d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_me', sa.String(length=250), nullable=True))
    op.add_column('users', sa.Column('profile_image', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_image')
    op.drop_column('users', 'about_me')
    # ### end Alembic commands ###
