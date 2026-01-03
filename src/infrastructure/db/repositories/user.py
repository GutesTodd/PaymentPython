from sqlalchemy import select

from domain.entities import User
from infrastructure.db.models.user import UserORM
from infrastructure.db.mapper import Mapper

from .base import BaseRepository

class UserRepository(BaseRepository[UserORM, User]):
    async def get_by_tg_id(self, telegram_id: int) -> User | None:
        stmt = select(self.orm_model).where(self.orm_model.tg_id == telegram_id)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        return Mapper.to_domain(orm_obj, self.entity_model)
