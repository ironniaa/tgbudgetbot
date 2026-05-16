from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    owner = Column(String)

    category = Column(String)

    amount = Column(Float)

    comment = Column(String)

    synced = Column(Boolean, default=False)