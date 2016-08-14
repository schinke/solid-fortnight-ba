"""empty message

Revision ID: 48471116cc35
Revises: 43fd8c6dfbf2
Create Date: 2016-08-10 09:34:02.364845

"""

# revision identifiers, used by Alembic.
revision = '48471116cc35'
down_revision = '43fd8c6dfbf2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('co2', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'co2', 'product', ['product_id'], ['id'])
    op.add_column('density', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'density', 'product', ['product_id'], ['id'])
    op.add_column('foodwaste', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'foodwaste', 'product', ['product_id'], ['id'])
    op.add_column('prod_allergene_association', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'prod_allergene_association', 'product', ['product_id'], ['id'])
    op.add_column('prod_nutrient_association', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'prod_nutrient_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.add_column('prod_process_association', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'prod_process_association', 'product', ['product_id'], ['id'])
    op.add_column('prod_process_co2_association', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'prod_process_co2_association', 'product', ['product_id'], ['id'])
    op.drop_constraint(u'scivalue_product_id_fkey', 'scivalue', type_='foreignkey')
    op.drop_column('scivalue', 'product_id')
    op.add_column('unit_weight', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'unit_weight', 'product', ['product_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit_weight', type_='foreignkey')
    op.drop_column('unit_weight', 'product_id')
    op.add_column('scivalue', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'scivalue_product_id_fkey', 'scivalue', 'product', ['product_id'], ['id'], ondelete=u'CASCADE')
    op.drop_constraint(None, 'prod_process_co2_association', type_='foreignkey')
    op.drop_column('prod_process_co2_association', 'product_id')
    op.drop_constraint(None, 'prod_process_association', type_='foreignkey')
    op.drop_column('prod_process_association', 'product_id')
    op.drop_constraint(None, 'prod_nutrient_association', type_='foreignkey')
    op.drop_column('prod_nutrient_association', 'product_id')
    op.drop_constraint(None, 'prod_allergene_association', type_='foreignkey')
    op.drop_column('prod_allergene_association', 'product_id')
    op.drop_constraint(None, 'foodwaste', type_='foreignkey')
    op.drop_column('foodwaste', 'product_id')
    op.drop_constraint(None, 'density', type_='foreignkey')
    op.drop_column('density', 'product_id')
    op.drop_constraint(None, 'co2', type_='foreignkey')
    op.drop_column('co2', 'product_id')
    ### end Alembic commands ###