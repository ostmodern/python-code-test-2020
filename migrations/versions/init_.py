"""empty message

Revision ID: 171bddf25626
Revises:
Create Date: 2021-01-28 07:48:31.967020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('episodes',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
                    sa.Column('released', sa.DATE(), nullable=True),
                    sa.Column('season', sa.INTEGER()),
                    sa.Column('episode', sa.INTEGER()),
                    sa.Column('imdb_rating', sa.NUMERIC(2, 1)),
                    sa.Column('imdb_id', sa.VARCHAR(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id', name='episodes_pkey'),
                    sa.UniqueConstraint("id"),
                    )
    op.create_table('comments',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('text', sa.Text()),
                    sa.Column('timestamp', sa.DateTime()),
                    sa.Column('episode_id', sa.Integer()),
                    sa.ForeignKeyConstraint(['episode_id'], ['episodes.id'], name='comments_episode_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='comments_pkey'),
                    )

    op.create_index('ix_episodes_imdb_id', 'episodes', ['imdb_id'], unique=True)


def downgrade():
    op.drop_table('episodes')
    op.drop_table('comments')