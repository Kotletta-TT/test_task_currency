import datetime

from sqlalchemy import create_engine, MetaData, DateTime, Table
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TEST_CUR = ["EUR", "USD"]

engine = create_engine('sqlite:///currency.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)


# session = Session()

class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_name = Column(String(4), nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, currency_name, value):
        self.currency_name = currency_name
        self.value = value


Base.metadata.create_all(engine)
