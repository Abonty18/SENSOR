"""Add is_active column to CSVFile

Revision ID: d92754aee937
Revises: e0741890004a
Create Date: 2024-12-20 02:37:23.776381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd92754aee937'
down_revision = 'e0741890004a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('csv_file', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('csv_file', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
