from sqlalchemy import select

from domain.entities import Subscription, SubscriptionPlan
from infrastructure.db.models.subscription import SubscriptionORM, SubscriptionPlanORM
from infrastructure.db.mapper import Mapper

from .base import BaseRepository

class SubscriptionRepository(BaseRepository[SubscriptionORM, Subscription]):
    async def get_by_user_id(self, user_id: int) -> Subscription | None:
        stmt = select(self.orm_model).where(self.orm_model.user_id == user_id)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()
        return Mapper.to_domain(obj, self.entity_model)

class SubscriptionPlanRepository(BaseRepository[SubscriptionPlanORM, SubscriptionPlan]):
    ...