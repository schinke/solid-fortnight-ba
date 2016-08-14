"""empty message

Revision ID: d9bfd5af0db2
Revises: a3143946c713
Create Date: 2016-08-10 00:18:21.079118

"""

# revision identifiers, used by Alembic.
revision = 'd9bfd5af0db2'
down_revision = 'a3143946c713'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'co2_id_fkey', 'co2', type_='foreignkey')
    op.create_foreign_key(None, 'co2', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'density_id_fkey', 'density', type_='foreignkey')
    op.create_foreign_key(None, 'density', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'foodwaste_id_fkey', 'foodwaste', type_='foreignkey')
    op.create_foreign_key(None, 'foodwaste', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'location_scivalue_association_scivalue_id_fkey', 'location_scivalue_association', type_='foreignkey')
    op.create_foreign_key(None, 'location_scivalue_association', 'scivalue', ['scivalue_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_allergene_association_id_fkey', 'prod_allergene_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_allergene_association', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_nutrient_association_id_fkey', 'prod_nutrient_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_nutrient_association', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_process_association_id_fkey', 'prod_process_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_process_association', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_process_co2_association_id_fkey', 'prod_process_co2_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_process_co2_association', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'unit_weight_id_fkey', 'unit_weight', type_='foreignkey')
    op.create_foreign_key(None, 'unit_weight', 'scivalue', ['id'], ['id'], ondelete='CASCADE')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit_weight', type_='foreignkey')
    op.create_foreign_key(u'unit_weight_id_fkey', 'unit_weight', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'prod_process_co2_association', type_='foreignkey')
    op.create_foreign_key(u'prod_process_co2_association_id_fkey', 'prod_process_co2_association', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'prod_process_association', type_='foreignkey')
    op.create_foreign_key(u'prod_process_association_id_fkey', 'prod_process_association', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'prod_nutrient_association', type_='foreignkey')
    op.create_foreign_key(u'prod_nutrient_association_id_fkey', 'prod_nutrient_association', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'prod_allergene_association', type_='foreignkey')
    op.create_foreign_key(u'prod_allergene_association_id_fkey', 'prod_allergene_association', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'location_scivalue_association', type_='foreignkey')
    op.create_foreign_key(u'location_scivalue_association_scivalue_id_fkey', 'location_scivalue_association', 'scivalue', ['scivalue_id'], ['id'])
    op.drop_constraint(None, 'foodwaste', type_='foreignkey')
    op.create_foreign_key(u'foodwaste_id_fkey', 'foodwaste', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'density', type_='foreignkey')
    op.create_foreign_key(u'density_id_fkey', 'density', 'scivalue', ['id'], ['id'])
    op.drop_constraint(None, 'co2', type_='foreignkey')
    op.create_foreign_key(u'co2_id_fkey', 'co2', 'scivalue', ['id'], ['id'])
    ### end Alembic commands ###