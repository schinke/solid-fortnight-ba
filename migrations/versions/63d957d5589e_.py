"""empty message

Revision ID: 63d957d5589e
Revises: 546054c4280d
Create Date: 2016-07-05 12:47:09.416179

"""

# revision identifiers, used by Alembic.
revision = '63d957d5589e'
down_revision = '546054c4280d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.drop_column('results', 'result_all')
    op.drop_column('results', 'result_no_stop_words')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('result_no_stop_words', postgresql.JSON(), autoincrement=False, nullable=True))
    op.add_column('results', sa.Column('result_all', postgresql.JSON(), autoincrement=False, nullable=True))
    op.drop_column('results', 'timestamp')
    ### end Alembic commands ###
