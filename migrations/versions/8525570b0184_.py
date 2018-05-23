"""empty message

Revision ID: 8525570b0184
Revises: ba2e493adec6
Create Date: 2018-05-20 08:16:45.236662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8525570b0184'
down_revision = 'ba2e493adec6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tmp_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_url', sa.String(length=80), nullable=True),
    sa.Column('img_url', sa.String(length=80), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tmp_data_timestamp'), 'tmp_data', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tmp_data_timestamp'), table_name='tmp_data')
    op.drop_table('tmp_data')
    # ### end Alembic commands ###
