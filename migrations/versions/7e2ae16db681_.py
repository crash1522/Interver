"""empty message

Revision ID: 7e2ae16db681
Revises: 
Create Date: 2024-03-25 14:20:56.506140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e2ae16db681'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('field', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('userid', name=op.f('uq_user_userid'))
    )
    op.create_table('record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.String(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], name=op.f('fk_record_userid_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_record'))
    )
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skill_name', sa.String(), nullable=False),
    sa.Column('userid', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], name=op.f('fk_skill_userid_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_skill'))
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['record_id'], ['record.id'], name=op.f('fk_question_record_id_record')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question'))
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('userid', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_answer_question_id_question')),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], name=op.f('fk_answer_userid_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_answer'))
    )
    op.create_table('question_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_question_voter_question_id_question')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_question_voter_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'question_id', name=op.f('pk_question_voter'))
    )
    op.create_table('answer_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], name=op.f('fk_answer_voter_answer_id_answer')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_answer_voter_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'answer_id', name=op.f('pk_answer_voter'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer_voter')
    op.drop_table('question_voter')
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('skill')
    op.drop_table('record')
    op.drop_table('user')
    # ### end Alembic commands ###
