"""empty message

Revision ID: af5c96902a03
Revises: 8bc97a172de1
Create Date: 2016-09-21 21:53:11.857595

"""

# revision identifiers, used by Alembic.
revision = 'af5c96902a03'
down_revision = '8bc97a172de1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prod_process_association', sa.Column('product_id', sa.Integer(), nullable=False))
    op.drop_constraint(u'prod_process_association_process_id_fkey', 'prod_process_association', type_='foreignkey')
    op.drop_constraint(u'prod_process_association_id_fkey', 'prod_process_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_process_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'prod_process_association', 'process', ['process_id'], ['id'], ondelete='CASCADE')
    op.drop_column('prod_process_association', 'id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prod_process_association', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'prod_process_association', type_='foreignkey')
    op.drop_constraint(None, 'prod_process_association', type_='foreignkey')
    op.create_foreign_key(u'prod_process_association_id_fkey', 'prod_process_association', 'scivalue', ['id'], ['id'], ondelete=u'CASCADE')
    op.create_foreign_key(u'prod_process_association_process_id_fkey', 'prod_process_association', 'process', ['process_id'], ['id'])
    op.drop_column('prod_process_association', 'product_id')
    ### end Alembic commands ###
