"""empty message

Revision ID: 822560cb0074
Revises: b88775493739
Create Date: 2016-08-09 23:09:07.817777

"""

# revision identifiers, used by Alembic.
revision = '822560cb0074'
down_revision = 'b88775493739'

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
    op.create_foreign_key(None, 'prod_nutrient_association', 'product', ['product_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('prod_process_association', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'prod_process_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.add_column('prod_process_co2_association', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'prod_process_co2_association', 'product', ['product_id'], ['id'])
    op.add_column('unit_weight', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'unit_weight', 'product', ['product_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit_weight', type_='foreignkey')
    op.drop_column('unit_weight', 'product_id')
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