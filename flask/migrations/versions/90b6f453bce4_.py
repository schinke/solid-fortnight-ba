"""empty message

Revision ID: 90b6f453bce4
Revises: f8997c541a5e
Create Date: 2016-08-10 00:30:36.030056

"""

# revision identifiers, used by Alembic.
revision = '90b6f453bce4'
down_revision = 'f8997c541a5e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'density_product_id_fkey', 'density', type_='foreignkey')
    op.drop_column('density', 'product_id')
    op.drop_constraint(u'prod_allergene_association_product_id_fkey', 'prod_allergene_association', type_='foreignkey')
    op.drop_column('prod_allergene_association', 'product_id')
    op.drop_constraint(u'prod_nutrient_association_product_id_fkey', 'prod_nutrient_association', type_='foreignkey')
    op.drop_column('prod_nutrient_association', 'product_id')
    op.drop_constraint(u'prod_process_association_product_id_fkey', 'prod_process_association', type_='foreignkey')
    op.drop_column('prod_process_association', 'product_id')
    op.drop_constraint(u'prod_process_co2_association_product_id_fkey', 'prod_process_co2_association', type_='foreignkey')
    op.drop_column('prod_process_co2_association', 'product_id')
    op.drop_constraint(u'unit_weight_product_id_fkey', 'unit_weight', type_='foreignkey')
    op.drop_column('unit_weight', 'product_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit_weight', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'unit_weight_product_id_fkey', 'unit_weight', 'product', ['product_id'], ['id'])
    op.add_column('prod_process_co2_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_process_co2_association_product_id_fkey', 'prod_process_co2_association', 'product', ['product_id'], ['id'])
    op.add_column('prod_process_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_process_association_product_id_fkey', 'prod_process_association', 'product', ['product_id'], ['id'])
    op.add_column('prod_nutrient_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_nutrient_association_product_id_fkey', 'prod_nutrient_association', 'product', ['product_id'], ['id'], ondelete=u'CASCADE')
    op.add_column('prod_allergene_association', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'prod_allergene_association_product_id_fkey', 'prod_allergene_association', 'product', ['product_id'], ['id'])
    op.add_column('density', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'density_product_id_fkey', 'density', 'product', ['product_id'], ['id'])
    ### end Alembic commands ###
