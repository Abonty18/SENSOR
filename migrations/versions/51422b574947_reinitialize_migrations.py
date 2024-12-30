"""Reinitialize migrations

Revision ID: 51422b574947
Revises: 
Create Date: 2024-12-21 01:19:54.119363

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '51422b574947'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('annotation', schema=None) as batch_op:
        # Skip adding 'is_final' column if it already exists
        # Note: Adjust manually as Alembic doesn't support conditionally skipping columns
        pass

    with op.batch_alter_table('completed_review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('csv_file_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            'fk_completed_review_csv_file_id',
            'csv_file',
            ['csv_file_id'],
            ['id']
        )

    with op.batch_alter_table('csv_file', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uploaded_by', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.create_foreign_key(
            'fk_csv_file_uploaded_by_user',
            'user',
            ['uploaded_by'],
            ['id']
        )

    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.Boolean(), nullable=True))

def downgrade():
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_column('completed')

    with op.batch_alter_table('csv_file', schema=None) as batch_op:
        batch_op.drop_constraint('fk_csv_file_uploaded_by_user', type_='foreignkey')
        batch_op.drop_column('is_active')
        batch_op.drop_column('uploaded_by')

    with op.batch_alter_table('completed_review', schema=None) as batch_op:
        batch_op.drop_constraint('fk_completed_review_csv_file_id', type_='foreignkey')
        batch_op.drop_column('csv_file_id')

    # Don't drop the 'is_final' column during downgrade if it already existed
    with op.batch_alter_table('annotation', schema=None) as batch_op:
        pass
