"""empty message

Revision ID: 9ca52745fa9e
Revises: b79fdb768212
Create Date: 2016-09-19 23:29:52.863926

"""

# revision identifiers, used by Alembic.
revision = '9ca52745fa9e'
down_revision = 'b79fdb768212'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prod_process_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['scivalue.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['process_id'], ['process.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prod_process_association')
    ### end Alembic commands ###