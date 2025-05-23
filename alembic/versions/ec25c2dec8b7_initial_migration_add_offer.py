"""Initial migration - Add Offer

Revision ID: ec25c2dec8b7
Revises: 
Create Date: 2025-05-06 21:51:46.067128

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = 'ec25c2dec8b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('price', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('size', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('rooms', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('year_built', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('heating', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('building_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('material', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('rent', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('ownership', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('condition', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('elevator', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('media', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('source', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('heating_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('floor_number', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('maintenance_cost', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('finishing_state', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('market_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('ownership_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('advertiser_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('additional_info', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('construction_year', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('has_elevator', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('building_type_detail', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('window_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('security', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('safety_features', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('offer')
    # ### end Alembic commands ###
