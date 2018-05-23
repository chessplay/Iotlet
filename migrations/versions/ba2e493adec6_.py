"""empty message

Revision ID: ba2e493adec6
Revises: 
Create Date: 2018-05-20 03:57:00.791330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba2e493adec6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appname', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=40), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('Appaddr', sa.String(length=20), nullable=True),
    sa.Column('flow', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('controller', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_timestamp'), 'app', ['timestamp'], unique=False)
    op.create_table('tmp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appname', sa.String(length=40), nullable=True),
    sa.Column('serveraddr', sa.String(length=40), nullable=True),
    sa.Column('rtmpaddr', sa.String(length=40), nullable=True),
    sa.Column('controller', sa.String(length=40), nullable=True),
    sa.Column('module', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.create_table('data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('video_url', sa.String(length=40), nullable=True),
    sa.Column('img_url', sa.String(length=40), nullable=True),
    sa.Column('other1', sa.String(length=40), nullable=True),
    sa.Column('other2', sa.String(length=40), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('app_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['app.id'], ),
    sa.PrimaryKeyConstraint('id', 'name')
    )
    op.create_index(op.f('ix_data_timestamp'), 'data', ['timestamp'], unique=False)
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('devicename', sa.String(length=20), nullable=True),
    sa.Column('pinnames', sa.String(length=40), nullable=True),
    sa.Column('app_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['app.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pinname', sa.String(length=10), nullable=True),
    sa.Column('connections', sa.Integer(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pin')
    op.drop_table('device')
    op.drop_index(op.f('ix_data_timestamp'), table_name='data')
    op.drop_table('data')
    op.drop_index(op.f('ix_tmp_data_timestamp'), table_name='tmp_data')
    op.drop_table('tmp_data')
    op.drop_table('tmp')
    op.drop_index(op.f('ix_app_timestamp'), table_name='app')
    op.drop_table('app')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
