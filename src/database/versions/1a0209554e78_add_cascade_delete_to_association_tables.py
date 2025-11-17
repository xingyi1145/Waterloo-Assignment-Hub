"""Add cascade delete to association tables

Revision ID: 1a0209554e78
Revises: 724f09d64704
Create Date: 2025-11-16 13:03:36.168127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a0209554e78'
down_revision: Union[str, None] = '724f09d64704'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # For SQLite, we need to recreate the tables with the new constraints
    with op.batch_alter_table('user_courses', schema=None) as batch_op:
        batch_op.drop_constraint('user_courses_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('user_courses_course_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('user_courses_user_id_fkey', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('user_courses_course_id_fkey', 'courses', ['course_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('user_solution_likes', schema=None) as batch_op:
        batch_op.drop_constraint('user_solution_likes_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('user_solution_likes_solution_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('user_solution_likes_user_id_fkey', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('user_solution_likes_solution_id_fkey', 'solutions', ['solution_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    # Revert to constraints without CASCADE
    with op.batch_alter_table('user_solution_likes', schema=None) as batch_op:
        batch_op.drop_constraint('user_solution_likes_solution_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('user_solution_likes_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('user_solution_likes_solution_id_fkey', 'solutions', ['solution_id'], ['id'])
        batch_op.create_foreign_key('user_solution_likes_user_id_fkey', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('user_courses', schema=None) as batch_op:
        batch_op.drop_constraint('user_courses_course_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('user_courses_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('user_courses_user_id_fkey', 'users', ['user_id'], ['id'])
        batch_op.create_foreign_key('user_courses_course_id_fkey', 'courses', ['course_id'], ['id'])
