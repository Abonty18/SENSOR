"""Add csv_file_id to CompletedReview

Revision ID: 3b0935d92dfc
Revises: d92754aee937
Create Date: 2024-12-20 02:54:07.865365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b0935d92dfc'
down_revision = 'd92754aee937'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('completed_review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('csv_file_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_completedreview_csvfile',  # Add a unique name for the foreign key
            'csv_file',
            ['csv_file_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('completed_review', schema=None) as batch_op:
        batch_op.drop_constraint('fk_completedreview_csvfile', type_='foreignkey')
        batch_op.drop_column('csv_file_id')

    # ### end Alembic commands ###
