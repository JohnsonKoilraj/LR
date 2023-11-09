"""initial migration

Revision ID: 238c535d31bb
Revises: 15d84b2f955c
Create Date: 2023-11-08 10:27:17.526187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '238c535d31bb'
down_revision: Union[str, None] = '15d84b2f955c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consignor_copy', sa.Column('gst_no', sa.String(length=20), nullable=True))
    op.add_column('consignor_copy', sa.Column('cin', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('consignor_copy', 'cin')
    op.drop_column('consignor_copy', 'gst_no')
    # ### end Alembic commands ###
