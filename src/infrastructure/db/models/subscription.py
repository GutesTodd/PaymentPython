import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import BaseORMModel

class SubscriptionPlanORM(BaseORMModel):
    __tablename__ = "subscription_plans"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=8))
    duration_days: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)


class SubscriptionORM(BaseORMModel):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    plan_id: Mapped[str | None] = mapped_column(ForeignKey("subscription_plans.id"), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(index=True)

    user: Mapped["UserORM"] = relationship(back_populates="subscription")