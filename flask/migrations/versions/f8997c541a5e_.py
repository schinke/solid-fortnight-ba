"""empty message

Revision ID: f8997c541a5e
Revises: 2a4195d55b40
Create Date: 2016-08-10 00:26:41.416391

"""

# revision identifiers, used by Alembic.
revision = 'f8997c541a5e'
down_revision = '2a4195d55b40'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scivalue', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'scivalue', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scivalue', type_='foreignkey')
    op.drop_column('scivalue', 'product_id')
    ### end Alembic commands ###
