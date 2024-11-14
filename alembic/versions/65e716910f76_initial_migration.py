"""initial migration

Revision ID: 65e716910f76
Revises: 7e3951d74b04
Create Date: 2024-11-14 02:58:46.196703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65e716910f76'
down_revision: Union[str, None] = '7e3951d74b04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coords_id'), 'coords', ['id'], unique=False)
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    op.create_table('level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('winter', sa.String(), nullable=True),
    sa.Column('summer', sa.String(), nullable=True),
    sa.Column('autumn', sa.String(), nullable=True),
    sa.Column('spring', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_level_id'), 'level', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('fam', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('otc', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('pereval_added',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('beauty_title', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('other_titles', sa.String(), nullable=True),
    sa.Column('connect', sa.String(), nullable=True),
    sa.Column('add_time', sa.String(), nullable=True),
    sa.Column('coord_id', sa.Integer(), nullable=True),
    sa.Column('level_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['coord_id'], ['coords.id'], ),
    sa.ForeignKeyConstraint(['level_id'], ['level.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pereval_added_id'), 'pereval_added', ['id'], unique=False)
    op.create_table('pereval_images',
    sa.Column('pereval_id', sa.Integer(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['pereval_id'], ['pereval_added.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pereval_images')
    op.drop_index(op.f('ix_pereval_added_id'), table_name='pereval_added')
    op.drop_table('pereval_added')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_level_id'), table_name='level')
    op.drop_table('level')
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('ix_coords_id'), table_name='coords')
    op.drop_table('coords')
    # ### end Alembic commands ###
