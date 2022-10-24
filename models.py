from my_engine import my_session
from sqlalchemy import Column, Integer, String, DateTime, Float, TIMESTAMP,text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    ticker = Column(String, nullable=False)


class Rate(Base):
    __tablename__ = 'rate'

    id = Column(Integer(), primary_key=True, unique=True)
    currency_id = Column(Integer())
    value = Column(Float(),  nullable = False)
    datetime = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
