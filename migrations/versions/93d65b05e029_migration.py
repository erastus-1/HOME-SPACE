"""migration

Revision ID: 93d65b05e029
Revises: 
Create Date: 2020-12-17 19:07:49.151137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d65b05e029'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('houses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.String(length=4), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('types', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_houses_types'), 'houses', ['types'], unique=False)
    op.create_index(op.f('ix_houses_year'), 'houses', ['year'], unique=False)
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('code', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('houselanguages',
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('types', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['house_id'], ['houses.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ),
    sa.PrimaryKeyConstraint('house_id', 'language_id')
    )
    op.create_index(op.f('ix_houselanguages_types'), 'houselanguages', ['types'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('date_entered', sa.String(length=32), nullable=True),
    sa.Column('date_out', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_date_entered'), 'users', ['date_entered'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_timestamp'), 'users', ['timestamp'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('house', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['house'], ['houses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userhouses',
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('houses_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['houses_id'], ['houses.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('users_id', 'houses_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userhouses')
    op.drop_table('comments')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_timestamp'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_date_entered'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_houselanguages_types'), table_name='houselanguages')
    op.drop_table('houselanguages')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_table('languages')
    op.drop_index(op.f('ix_houses_year'), table_name='houses')
    op.drop_index(op.f('ix_houses_types'), table_name='houses')
    op.drop_table('houses')
    # ### end Alembic commands ###
