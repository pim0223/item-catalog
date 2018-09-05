"""Added created_by to each item

Revision ID: f8eb1fa3bc4d
Revises: 
Create Date: 2018-09-04 16:57:25.610041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8eb1fa3bc4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'item', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_column('item', 'created_by')
    # ### end Alembic commands ###
