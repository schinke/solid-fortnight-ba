"""empty message

Revision ID: 2018d552dff6
Revises: 7c2027d938af
Create Date: 2016-08-14 10:51:12.274004

"""

# revision identifiers, used by Alembic.
revision = '2018d552dff6'
down_revision = '7c2027d938af'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scivalue', sa.Column('comment', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scivalue', 'comment')
    ### end Alembic commands ###
