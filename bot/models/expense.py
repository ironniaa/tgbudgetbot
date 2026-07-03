from typing import Optional

from sqlalchemy import Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from zoneinfo import ZoneInfo

from bot.config import TIMEZONE


class Base(DeclarativeBase):
    pass


def _now_minsk():
    return datetime.now(ZoneInfo(TIMEZONE))


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now_minsk
    )

    timezone: Mapped[str] = mapped_column(String, default=TIMEZONE)

    type: Mapped[str] = mapped_column(String, default="expense")

    creator: Mapped[str] = mapped_column(String)

    owner: Mapped[str] = mapped_column(String)

    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    amount: Mapped[float] = mapped_column(Float)

    comment: Mapped[str] = mapped_column(String)

    synced: Mapped[bool] = mapped_column(Boolean, default=False)