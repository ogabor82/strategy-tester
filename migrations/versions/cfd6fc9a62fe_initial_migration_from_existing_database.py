"""Initial migration from existing database

Revision ID: cfd6fc9a62fe
Revises: 
Create Date: 2025-01-10 10:59:58.118013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd6fc9a62fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project')
    op.drop_table('timeframe_set')
    op.drop_table('backtest_slice')
    op.drop_table('strategy')
    op.drop_table('timeframe')
    op.drop_table('optimization_session')
    op.drop_table('backtest_session')
    op.drop_table('optimization_slice')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('optimization_slice',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('optimization_session_id', sa.INTEGER(), nullable=True),
    sa.Column('timeframe_id', sa.INTEGER(), nullable=True),
    sa.Column('strategy_id', sa.INTEGER(), nullable=True),
    sa.Column('ticker', sa.VARCHAR(), nullable=True),
    sa.Column('start', sa.DATETIME(), nullable=True),
    sa.Column('end', sa.DATETIME(), nullable=True),
    sa.Column('interval', sa.VARCHAR(), nullable=True),
    sa.Column('optimization_results', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('backtest_session',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('details', sa.VARCHAR(), nullable=True),
    sa.Column('project_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('optimization_session',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('details', sa.VARCHAR(), nullable=True),
    sa.Column('project_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timeframe',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('timeframe_set_id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('start', sa.DATETIME(), nullable=True),
    sa.Column('end', sa.DATETIME(), nullable=True),
    sa.Column('interval', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strategy',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('backtest_sets', sa.VARCHAR(), nullable=True),
    sa.Column('optimization_sets', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('backtest_slice',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('backtest_session_id', sa.INTEGER(), nullable=True),
    sa.Column('configuration_id', sa.INTEGER(), nullable=True),
    sa.Column('strategy_id', sa.INTEGER(), nullable=True),
    sa.Column('strategy_parameters', sa.VARCHAR(), nullable=True),
    sa.Column('ticker', sa.VARCHAR(), nullable=True),
    sa.Column('start', sa.DATETIME(), nullable=True),
    sa.Column('end', sa.DATETIME(), nullable=True),
    sa.Column('interval', sa.VARCHAR(), nullable=True),
    sa.Column('return', sa.FLOAT(), nullable=True),
    sa.Column('buyhold_return', sa.FLOAT(), nullable=True),
    sa.Column('max_drawdown', sa.FLOAT(), nullable=True),
    sa.Column('trades', sa.INTEGER(), nullable=True),
    sa.Column('win_rate', sa.FLOAT(), nullable=True),
    sa.Column('sharpe_ratio', sa.FLOAT(), nullable=True),
    sa.Column('kelly_criterion', sa.FLOAT(), nullable=True),
    sa.Column('filename', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timeframe_set',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('goal', sa.VARCHAR(), nullable=True),
    sa.Column('details', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
