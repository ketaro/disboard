"""Initial

Revision ID: 32af359a80e1
Revises: 
Create Date: 2015-08-17 22:38:10.440770

"""

# revision identifiers, used by Alembic.
revision = '32af359a80e1'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('givenname', sa.String(length=30), nullable=True),
    sa.Column('surname', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('tos_agree', sa.Integer(), nullable=True),
    sa.Column('verified', sa.Integer(), nullable=True),
    sa.Column('last_login', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.String(length=120), nullable=False),
    sa.Column('updated_at', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive'), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_category_id'), 'questions', ['category_id'], unique=False)
    op.create_table('slides',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slide_type', sa.Enum('title', 'text', 'choice', 'video'), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('prompt', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_slides_question_id'), 'slides', ['question_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_slides_question_id'), table_name='slides')
    op.drop_table('slides')
    op.drop_index(op.f('ix_questions_category_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_table('categories')
    ### end Alembic commands ###
