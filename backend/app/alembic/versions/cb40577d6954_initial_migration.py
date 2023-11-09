"""initial migration

Revision ID: cb40577d6954
Revises: 
Create Date: 2023-11-06 15:07:21.733699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'cb40577d6954'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consignee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('mobile_no', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-active,2-inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consignor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('mobile_no', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-active,2-inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consignor_copy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insurance', mysql.TINYINT(), nullable=True, comment="1-Owner's Risk,2-Carrier's Risk"),
    sa.Column('insurer', sa.String(length=50), nullable=True),
    sa.Column('policy_no', sa.String(length=50), nullable=True),
    sa.Column('policy_dt', sa.String(length=50), nullable=True),
    sa.Column('policy_rs', sa.String(length=50), nullable=True),
    sa.Column('risk_rs', sa.String(length=50), nullable=True),
    sa.Column('gc_no', sa.String(length=50), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('vehicle_no', sa.String(length=50), nullable=True),
    sa.Column('e_way_bill', sa.String(length=50), nullable=True),
    sa.Column('from_date', sa.DateTime(), nullable=True),
    sa.Column('to_date', sa.DateTime(), nullable=True),
    sa.Column('delivery_instruction', sa.String(length=250), nullable=True),
    sa.Column('booking_type', mysql.TINYINT(), nullable=True, comment='1-Full Truck Load,2-Part Load,3-Miscellaneous'),
    sa.Column('consignor_id', sa.Integer(), nullable=True),
    sa.Column('consignee_id', sa.Integer(), nullable=True),
    sa.Column('consignor_gst', sa.String(length=50), nullable=True),
    sa.Column('consignee_gst', sa.String(length=50), nullable=True),
    sa.Column('packages', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.Column('actual_weight', sa.String(length=50), nullable=True),
    sa.Column('chargeable_weight', sa.String(length=50), nullable=True),
    sa.Column('rate_kg', sa.String(length=50), nullable=True),
    sa.Column('basis_of_freight', mysql.TINYINT(), nullable=True, comment='1-paid,2-to be filled,3-to pay'),
    sa.Column('rs', sa.String(length=50), nullable=True),
    sa.Column('declared_value_goods', sa.String(length=50), nullable=True),
    sa.Column('invoice_dc_no', sa.String(length=50), nullable=True),
    sa.Column('invoice_dc_dt', sa.String(length=50), nullable=True),
    sa.Column('receivers_name', sa.String(length=50), nullable=True),
    sa.Column('date_of_receipt', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1-active,2-inactive'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['consignee_id'], ['consignee.id'], ),
    sa.ForeignKeyConstraint(['consignor_id'], ['consignor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('consignor_copy')
    op.drop_table('consignor')
    op.drop_table('consignee')
    # ### end Alembic commands ###