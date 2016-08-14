"""empty message

Revision ID: df62be078722
Revises: 30ca04771e1d
Create Date: 2016-08-09 13:10:19.435723

"""

# revision identifiers, used by Alembic.
revision = 'df62be078722'
down_revision = '30ca04771e1d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'density_product_id_fkey', 'density', type_='foreignkey')
    op.create_foreign_key(None, 'density', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'edb_product_id_fkey', 'edb_product', type_='foreignkey')
    op.create_foreign_key(None, 'edb_product', 'product', ['id'], ['id'])
    op.drop_constraint(u'prod_allergene_association_product_id_fkey', 'prod_allergene_association', type_='foreignkey')
    op.drop_constraint(u'prod_allergene_association_allergene_id_fkey', 'prod_allergene_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_allergene_association', 'allergene', ['allergene_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'prod_allergene_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_nutrient_association_nutrient_id_fkey', 'prod_nutrient_association', type_='foreignkey')
    op.drop_constraint(u'prod_nutrient_association_product_id_fkey', 'prod_nutrient_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_nutrient_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'prod_nutrient_association', 'nutrient', ['nutrient_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_process_association_nutrient_id_fkey', 'prod_process_association', type_='foreignkey')
    op.drop_constraint(u'prod_process_association_process_id_fkey', 'prod_process_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_process_association', 'process', ['process_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'prod_process_association', 'nutrient', ['nutrient_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'prod_process_co2_association_product_id_fkey', 'prod_process_co2_association', type_='foreignkey')
    op.drop_constraint(u'prod_process_co2_association_process_id_fkey', 'prod_process_co2_association', type_='foreignkey')
    op.create_foreign_key(None, 'prod_process_co2_association', 'process', ['process_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'prod_process_co2_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'synonym_prod_association_product_id_fkey', 'synonym_prod_association', type_='foreignkey')
    op.drop_constraint(u'synonym_prod_association_synonym_name_fkey', 'synonym_prod_association', type_='foreignkey')
    op.create_foreign_key(None, 'synonym_prod_association', 'synonym', ['synonym_name'], ['name'], ondelete='CASCADE')
    op.create_foreign_key(None, 'synonym_prod_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(u'template_id_fkey', 'template', type_='foreignkey')
    op.create_foreign_key(None, 'template', 'product', ['id'], ['id'])
    op.drop_constraint(u'unit_weight_product_id_fkey', 'unit_weight', type_='foreignkey')
    op.create_foreign_key(None, 'unit_weight', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit_weight', type_='foreignkey')
    op.create_foreign_key(u'unit_weight_product_id_fkey', 'unit_weight', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'template', type_='foreignkey')
    op.create_foreign_key(u'template_id_fkey', 'template', 'product', ['id'], ['id'], ondelete=u'CASCADE')
    op.drop_constraint(None, 'synonym_prod_association', type_='foreignkey')
    op.drop_constraint(None, 'synonym_prod_association', type_='foreignkey')
    op.create_foreign_key(u'synonym_prod_association_synonym_name_fkey', 'synonym_prod_association', 'synonym', ['synonym_name'], ['name'])
    op.create_foreign_key(u'synonym_prod_association_product_id_fkey', 'synonym_prod_association', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'prod_process_co2_association', type_='foreignkey')
    op.drop_constraint(None, 'prod_process_co2_association', type_='foreignkey')
    op.create_foreign_key(u'prod_process_co2_association_process_id_fkey', 'prod_process_co2_association', 'process', ['process_id'], ['id'])
    op.create_foreign_key(u'prod_process_co2_association_product_id_fkey', 'prod_process_co2_association', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'prod_process_association', type_='foreignkey')
    op.drop_constraint(None, 'prod_process_association', type_='foreignkey')
    op.create_foreign_key(u'prod_process_association_process_id_fkey', 'prod_process_association', 'process', ['process_id'], ['id'])
    op.create_foreign_key(u'prod_process_association_nutrient_id_fkey', 'prod_process_association', 'nutrient', ['nutrient_id'], ['id'])
    op.drop_constraint(None, 'prod_nutrient_association', type_='foreignkey')
    op.drop_constraint(None, 'prod_nutrient_association', type_='foreignkey')
    op.create_foreign_key(u'prod_nutrient_association_product_id_fkey', 'prod_nutrient_association', 'product', ['product_id'], ['id'])
    op.create_foreign_key(u'prod_nutrient_association_nutrient_id_fkey', 'prod_nutrient_association', 'nutrient', ['nutrient_id'], ['id'])
    op.drop_constraint(None, 'prod_allergene_association', type_='foreignkey')
    op.drop_constraint(None, 'prod_allergene_association', type_='foreignkey')
    op.create_foreign_key(u'prod_allergene_association_allergene_id_fkey', 'prod_allergene_association', 'allergene', ['allergene_id'], ['id'])
    op.create_foreign_key(u'prod_allergene_association_product_id_fkey', 'prod_allergene_association', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'edb_product', type_='foreignkey')
    op.create_foreign_key(u'edb_product_id_fkey', 'edb_product', 'product', ['id'], ['id'], ondelete=u'CASCADE')
    op.drop_constraint(None, 'density', type_='foreignkey')
    op.create_foreign_key(u'density_product_id_fkey', 'density', 'product', ['product_id'], ['id'])
    ### end Alembic commands ###