from sqlalchemy import select

from src.domain.entities import Subscription, SubscriptionPlan
from src.domain.interfaces.repositories import ISubscriptionRepository, IPlanRepository
from infrastructure.db.models.subscription import SubscriptionORM, SubscriptionPlanORM
from .base import BaseRepository

class SubscriptionRepository(BaseRepository[SubscriptionORM], ISubscriptionRepository):
    async def get_by_user_id(self, user_id: int) -> Subscription | None:
        stmt = select(self.orm_model).where(self.orm_model.user_id == user_id)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()

        if not obj:
            return None
        return Subscription(
            user_id=obj.user_id,
            expires_at=obj.expires_at,
            plan_id=obj.plan_id
        )
    async def save(self, subscription: Subscription) -> Subscription:
        