from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseORMModel

class UserORM(BaseORMModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, index=True, nullable=True)
    username: Mapped[str | None]
    is_banned: Mapped[bool] = mapped_column(default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc)
                                                 )

    subscription: Mapped["SubscriptionORM | None"] = relationship(back_populates="user", cascade="all, delete-orphan")
    payments: Mapped[list["PaymentORM"]] = relationship(back_populates="user")


class RefreshTokenORM(BaseORMModel):
    __tablename__ = 'refresh_tokens'

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    refresh_token: Mapped[str] = mapped_column(String)
    expired_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    user: Mapped['UserORM'] = relationship('UserORM', back_populates='refresh_tokens')