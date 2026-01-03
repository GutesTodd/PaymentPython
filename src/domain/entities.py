from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from src.domain.exceptions import UserBannedException, InvalidPlanException, InvalidStatusTransition

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

@dataclass
class SubscriptionPlan:
    id: str
    name: str
    price: Decimal
    duration_days: int

    def __post_init__(self):
        if self.price <= 0:
            raise InvalidPlanException("Price must be greater than zero")
        if self.duration_days <= 0:
            raise InvalidPlanException("Duration must be at least 1 day")

@dataclass
class Subscription:
    user_id: int
    expires_at: datetime
    plan_id: Optional[str] = None

    @property
    def is_active(self) -> bool:
        return self.expires_at > datetime.utcnow()

@dataclass
class User:
    id: int
    tg_id: Optional[int] = None
    username: Optional[str] = None
    is_banned: bool = False

    def extend_subscription(self, current_sub: Optional[Subscription], plan: SubscriptionPlan) -> Subscription:
        """Бизнес-логика продления подписки."""
        if self.is_banned:
            raise UserBannedException(f"User {self.id} is banned")

        now = datetime.utcnow()
        if current_sub and current_sub.is_active:
            base_date = current_sub.expires_at
        else:
            base_date = now

        new_expiry = base_date + timedelta(days=plan.duration_days)
        
        return Subscription(
            user_id=self.id,
            plan_id=plan.id,
            expires_at=new_expiry
        )

@dataclass
class Payment:
    id: str
    user_id: int
    plan_id: str
    amount: Decimal
    external_id: int
    status: PaymentStatus = PaymentStatus.PENDING
    pay_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def mark_as_paid(self):
        if self.status != PaymentStatus.PENDING:
            raise InvalidStatusTransition(f"Cannot pay from state {self.status}")
        self.status = PaymentStatus.PAID