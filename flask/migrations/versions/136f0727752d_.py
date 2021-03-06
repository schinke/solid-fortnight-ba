"""empty message

Revision ID: 136f0727752d
Revises: 2eeb48dc8ec7
Create Date: 2016-08-09 17:45:02.499939

"""

# revision identifiers, used by Alembic.
revision = '136f0727752d'
down_revision = '2eeb48dc8ec7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'co2_product_id_fkey', 'co2', type_='foreignkey')
    op.drop_column('co2', 'product_id')
    op.drop_constraint(u'density_product_id_fkey', 'density', type_='foreignkey')
    op.drop_column('density', 'product_id')
    op.drop_constraint(u'foodwaste_product_id_fkey', 'foodwaste', type_='foreignkey')
    op.drop_column('foodwaste', 'product_id')
    op.drop_constraint(u'location_prod_association_product_id_fkey', 'location_prod_association', type_='foreignkey')
    op.create_foreign_key(None, 'location_prod_association', 'product', ['product_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(u'prod_allergene_association_product_id_fkey', 'prod_allergene_association', type_='foreignkey')
    op.drop_column('prod_allergene_association', 'product_id')
    op.drop_constraint(u'prod_nutrient_association_product_id_fkey', 'prod_nutrient_association', type_='foreignkey')
    op.drop_column('prod_nutrient_association', 'product_id')
    op.drop_constraint(u'prod_process_association_product_id_fkey', 'prod_process_association', type_='foreignkey')
    op.drop_column('prod_process_association', 'product_id')
    op.drop_constraint(u'prod_process_co2_association_product_id_fkey', 'prod_process_co2_association', type_='foreignkey')
    op.drop_column('prod_process_co2_association', 'product_id')
    op.add_column('scivalue', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'scivalue', 'product', ['product_id'], ['id'])
    op.drop_constraint(u'synonym_prod_association_product_id_fkey', 'synonym_prod_association', type_='foreignkey')
    op.create_foreign_key(None, 'synonym_prod_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'unit_weight_product_id_fkey', 'unit_weight', type_='foreignkey')
    op.drop_column('unit_weight', 'product_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit_weight', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'unit_weight_product_id_fkey', 'unit_weight', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'synonym_prod_association', type_='foreignkey')
    op.create_foreign_key(u'synonym_prod_association_product_id_fkey', 'synonym_prod_association', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'scivalue', type_='foreignkey')
    op.drop_column('scivalue', 'product_id')
    op.add_column('prod_process_co2_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_process_co2_association_product_id_fkey', 'prod_process_co2_association', 'product', ['product_id'], ['id'])
    op.add_column('prod_process_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_process_association_product_id_fkey', 'prod_process_association', 'product', ['product_id'], ['id'], ondelete=u'CASCADE')
    op.add_column('prod_nutrient_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_nutrient_association_product_id_fkey', 'prod_nutrient_association', 'product', ['product_id'], ['id'], onupdate=u'CASCADE', ondelete=u'CASCADE')
    op.add_column('prod_allergene_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_allergene_association_product_id_fkey', 'prod_allergene_association', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'location_prod_association', type_='foreignkey')
    op.create_foreign_key(u'location_prod_association_product_id_fkey', 'location_prod_association', 'product', ['product_id'], ['id'])
    op.add_column('foodwaste', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'foodwaste_product_id_fkey', 'foodwaste', 'product', ['product_id'], ['id'])
    op.add_column('density', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'density_product_id_fkey', 'density', 'product', ['product_id'], ['id'])
    op.add_column('co2', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'co2_product_id_fkey', 'co2', 'product', ['product_id'], ['id'])
    ### end Alembic commands ###
