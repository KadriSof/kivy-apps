"""Add diagnostic_reports table

Revision ID: 8da681a29bf8
Revises: 
Create Date: 2024-06-03 22:02:43.747798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8da681a29bf8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('devices', 'client_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.drop_index('devices_ibfk_2_idx', table_name='devices')
    op.drop_constraint('devices_ibfk_2', 'devices', type_='foreignkey')
    op.drop_column('devices', 'diagnostic_report_id')
    op.alter_column('diagnostic_reports', 'resolved',
               existing_type=mysql.TINYINT(),
               nullable=True)
    op.drop_index('reports_ibfk_1_idx', table_name='diagnostic_reports')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('reports_ibfk_1_idx', 'diagnostic_reports', ['device_id'], unique=False)
    op.alter_column('diagnostic_reports', 'resolved',
               existing_type=mysql.TINYINT(),
               nullable=False)
    op.add_column('devices', sa.Column('diagnostic_report_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('devices_ibfk_2', 'devices', 'diagnostic_reports', ['diagnostic_report_id'], ['id'])
    op.create_index('devices_ibfk_2_idx', 'devices', ['diagnostic_report_id'], unique=False)
    op.alter_column('devices', 'client_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
