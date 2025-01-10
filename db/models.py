# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BacktestSession(Base):
    __tablename__ = 'backtest_session'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    details = Column(String)
    project_id = Column(Integer)


class BacktestSlice(Base):
    __tablename__ = 'backtest_slice'

    id = Column(Integer, primary_key=True)
    backtest_session_id = Column(Integer)
    configuration_id = Column(Integer)
    strategy_id = Column(Integer)
    strategy_parameters = Column(String)
    ticker = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    interval = Column(String)
    _return = Column('return', Float)
    buyhold_return = Column(Float)
    max_drawdown = Column(Float)
    trades = Column(Integer)
    win_rate = Column(Float)
    sharpe_ratio = Column(Float)
    kelly_criterion = Column(Float)
    filename = Column(String)


class OptimizationSession(Base):
    __tablename__ = 'optimization_session'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    details = Column(String)
    project_id = Column(Integer)


class OptimizationSlice(Base):
    __tablename__ = 'optimization_slice'

    id = Column(Integer, primary_key=True)
    optimization_session_id = Column(Integer)
    timeframe_id = Column(Integer)
    strategy_id = Column(Integer)
    ticker = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    interval = Column(String)
    optimization_results = Column(String)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    goal = Column(String)
    details = Column(String)


class Strategy(Base):
    __tablename__ = 'strategy'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    backtest_sets = Column(String)
    optimization_sets = Column(String)


class Timeframe(Base):
    __tablename__ = 'timeframe'

    id = Column(Integer, primary_key=True)
    timeframe_set_id = Column(Integer)
    name = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    interval = Column(String)


class TimeframeSet(Base):
    __tablename__ = 'timeframe_set'

    id = Column(Integer, primary_key=True)
    name = Column(String)
