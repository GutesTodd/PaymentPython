import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import BaseORMModel

class UserORM(BaseORMModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, index=True, nullable=True)
    username: Mapped[str | None]
    is_banned: Mapped[bool] = mapped_column(default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    subscription: Mapped["SubscriptionORM" | None] = relationship(back_populates="user", cascade="all, delete-orphan")
    payments: Mapped[list["PaymentORM"]] = relationship(back_populates="user")