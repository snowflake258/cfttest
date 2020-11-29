from sqlalchemy import (
    MetaData, Table, Column,
    Integer, Float, Enum, ForeignKey, DateTime
)
from datetime import datetime
from db.enums import CountryEnum, CurrencyEnum


meta = MetaData()


limit = Table(
    'limit', meta,

    Column('id', Integer, primary_key=True),
    Column('country', Enum(CountryEnum), nullable=False),
    Column('currency', Enum(CurrencyEnum), nullable=False),
    Column('max_sum_per_month', Float, nullable=False)
)


transfer = Table(
    'transfer', meta,

    Column('id', Integer, primary_key=True),
    Column('time', DateTime, nullable=False, default=datetime.now()),
    Column('sum', Float, nullable=False),
    Column('country', Enum(CountryEnum), nullable=False),
    Column('currency', Enum(CurrencyEnum), nullable=False),
    Column('limit_id', Integer, ForeignKey('limit.id', ondelete='CASCADE'), nullable=False)
)
