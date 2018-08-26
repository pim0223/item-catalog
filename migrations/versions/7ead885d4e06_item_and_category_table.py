"""Item and category table

Revision ID: 7ead885d4e06
Revises: cf5ae8c4f151
Create Date: 2018-08-24 14:00:34.923664

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ead885d4e06'
down_revision = 'cf5ae8c4f151'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_created_at'), 'category', ['created_at'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_created_at'), 'item', ['created_at'], unique=False)
    op.create_index(op.f('ix_item_name'), 'item', ['name'], unique=True)
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_column('user', 'created_at')
    op.drop_index(op.f('ix_item_name'), table_name='item')
    op.drop_index(op.f('ix_item_created_at'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_created_at'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###