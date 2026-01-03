import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Enum as SQLEnum, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.domain.entities import PaymentStatus
from .base import BaseORMModel


class PaymentORM(BaseORMModel):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    plan_id: Mapped[str] = mapped_column(ForeignKey("subscription_plans.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=8))

    external_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus), 
        default=PaymentStatus.PENDING,
        native_enum=False
    )
    
    pay_url: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["UserORM"] = relationship(back_populates="payments")