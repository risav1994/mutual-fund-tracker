from sqlalchemy import Column, BIGINT, DateTime, BOOLEAN, INT, VARCHAR, TIMESTAMP, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MutualFunds(Base):
    __tablename__ = "mutual_funds"
    id = Column('id', BIGINT, primary_key=True, autoincrement=True, nullable=False)
    identifier = Column('identifier', VARCHAR(20), nullable=False)
    name = Column('name', VARCHAR(255), nullable=False)
    is_deleted = Column('is_deleted', BOOLEAN, nullable=False)
    created_at = Column('created_at', TIMESTAMP, nullable=False)
    updated_at = Column('updated_at', TIMESTAMP, nullable=False)


class InvestmentRecords(Base):
    __tablename__ = "investment_records"
    id = Column('id', BIGINT, primary_key=True, autoincrement=True, nullable=False)
    fund_identifier = Column('fund_identifier', VARCHAR(20), nullable=False)
    nav = Column('nav', FLOAT, nullable=False)
    units = Column('units', FLOAT, nullable=False)
    execution_date = Column('execution_date', TIMESTAMP, nullable=False)
    is_deleted = Column('is_deleted', BOOLEAN, nullable=False)
    created_at = Column('created_at', TIMESTAMP, nullable=False)
    updated_at = Column('updated_at', TIMESTAMP, nullable=False)


class NavHistories(Base):
    __tablename__ = "nav_histories"
    id = Column('id', BIGINT, primary_key=True, autoincrement=True, nullable=False)
    fund_identifier = Column('fund_identifier', VARCHAR(20), nullable=False)
    fund_name = Column('fund_name', VARCHAR(255), nullable=False)
    nav = Column('nav', FLOAT, nullable=False)
    date = Column('date', TIMESTAMP, nullable=False)
    is_deleted = Column('is_deleted', BOOLEAN, nullable=False)
    created_at = Column('created_at', TIMESTAMP, nullable=False)
    updated_at = Column('updated_at', TIMESTAMP, nullable=False)
