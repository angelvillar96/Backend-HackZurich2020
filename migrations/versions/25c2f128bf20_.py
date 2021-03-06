"""empty message

Revision ID: 25c2f128bf20
Revises: 1932f6341f82
Create Date: 2020-09-19 00:59:32.813826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25c2f128bf20'
down_revision = '1932f6341f82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food',
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('date_consumed', sa.DateTime(), nullable=True),
    sa.Column('calories', sa.Integer(), nullable=True),
    sa.Column('fat', sa.Integer(), nullable=True),
    sa.Column('protein', sa.Integer(), nullable=True),
    sa.Column('carbs', sa.Integer(), nullable=True),
    sa.Column('sugar', sa.Integer(), nullable=True),
    sa.Column('sodium', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('food_id')
    )
    op.create_index(op.f('ix_food_date_consumed'), 'food', ['date_consumed'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_food_date_consumed'), table_name='food')
    op.drop_table('food')
    # ### end Alembic commands ###
