from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    owner = Column(String)

    category: Mapped[str] = mapped_column(String)

    amount: Mapped[float] = mapped_column(Float)

    comment: Mapped[str] = mapped_column(String)

    synced: Mapped[bool] = mapped_column(Boolean, default=False)