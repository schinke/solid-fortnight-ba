"""empty message

Revision ID: e3c68e835c84
Revises: 71ea99d099f6
Create Date: 2016-08-18 16:54:43.257222

"""

# revision identifiers, used by Alembic.
revision = 'e3c68e835c84'
down_revision = '71ea99d099f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('euro4Id', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'euro4Id')
    ### end Alembic commands ###