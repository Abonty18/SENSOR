"""Validate schema after foreign key check

Revision ID: 7bb85f4c5718
Revises: ae1681318959
Create Date: 2024-12-23 19:34:12.238156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bb85f4c5718'
down_revision = 'ae1681318959'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('completed_review', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.create_foreign_key('fk_completed_review_annotator_1_id', 'user', ['annotator_1_id'], ['id'])
        batch_op.create_foreign_key('fk_completed_review_annotator_2_id', 'user', ['annotator_2_id'], ['id'])
        batch_op.create_foreign_key('fk_completed_review_annotator_3_id', 'user', ['annotator_3_id'], ['id'])

    with op.batch_alter_table('csv_file', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)

    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        try:
            batch_op.drop_column('completed')  # Drop column only if it exists
        except KeyError:
            pass  # Skip if the column does not exist

    with op.batch_alter_table('csv_file', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('completed_review', schema=None) as batch_op:
        batch_op.drop_constraint('fk_completed_review_annotator_1_id', type_='foreignkey')
        batch_op.drop_constraint('fk_completed_review_annotator_2_id', type_='foreignkey')
        batch_op.drop_constraint('fk_completed_review_annotator_3_id', type_='foreignkey')
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    try:
        op.create_table('_alembic_tmp_completed_review',
            sa.Column('id', sa.INTEGER(), nullable=True),
            sa.Column('text', sa.TEXT(), nullable=False),
            sa.Column('csv_file_id', sa.INTEGER(), nullable=False),
            sa.Column('annotator_1_id', sa.INTEGER(), nullable=True),
            sa.Column('annotation_1', sa.TEXT(), nullable=True),
            sa.Column('annotator_2_id', sa.INTEGER(), nullable=True),
            sa.Column('annotation_2', sa.TEXT(), nullable=True),
            sa.Column('annotator_3_id', sa.INTEGER(), nullable=True),
            sa.Column('annotation_3', sa.TEXT(), nullable=True),
            sa.Column('completed_at', sa.DATETIME(), nullable=True),
            sa.ForeignKeyConstraint(['annotator_1_id'], ['user.id'], name='fk_completed_review_annotator_1_id'),
            sa.ForeignKeyConstraint(['annotator_2_id'], ['user.id'], name='fk_completed_review_annotator_2_id'),
            sa.ForeignKeyConstraint(['annotator_3_id'], ['user.id'], name='fk_completed_review_annotator_3_id'),
            sa.ForeignKeyConstraint(['csv_file_id'], ['csv_file.id'], name='fk_completed_review_csv_file_id'),
            sa.PrimaryKeyConstraint('id')
        )
    except Exception as e:
        print(f"Skipping creation of _alembic_tmp_completed_review due to: {e}")

    # ### end Alembic commands ###