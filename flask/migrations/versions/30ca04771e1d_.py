"""empty message

Revision ID: 30ca04771e1d
Revises: 57128d66cc33
Create Date: 2016-08-09 12:53:07.598733

"""

# revision identifiers, used by Alembic.
revision = '30ca04771e1d'
down_revision = '57128d66cc33'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'edb_product_id_fkey', 'edb_product', type_='foreignkey')
    op.create_foreign_key(None, 'edb_product', 'product', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'template_id_fkey', 'template', type_='foreignkey')
    op.create_foreign_key(None, 'template', 'product', ['id'], ['id'], ondelete='CASCADE')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'template', type_='foreignkey')
    op.create_foreign_key(u'template_id_fkey', 'template', 'product', ['id'], ['id'])
    op.drop_constraint(None, 'edb_product', type_='foreignkey')
    op.create_foreign_key(u'edb_product_id_fkey', 'edb_product', 'product', ['id'], ['id'])
    ### end Alembic commands ###
