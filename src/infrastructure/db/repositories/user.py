from sqlalchemy import select

from domain.entities import User, RefreshToken
from infrastructure.db.models.user import UserORM
from infrastructure.db.mapper import Mapper

from .base import BaseRepository

class UserRepository(BaseRepository[UserORM, User]):
    async def get_by_tg_id(self, telegram_id: int) -> User | None:
        stmt = select(self.orm_model).where(self.orm_model.tg_id == telegram_id)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        return Mapper.to_domain(orm_obj, self.entity_model)
    
    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.orm_model).where(self.orm_model.username == username)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        return Mapper.to_domain(orm_obj, self.entity_model)
    
class RefreshTokenRepository(BaseRepository[RefreshTokenORM, RefreshToken]):
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        stmt = select(self.orm_model).where(self.orm_model.refresh_token == token)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        return Mapper.to_domain(orm_obj)

    async def delete_by_user_id(self, user_id: int) -> None:
        stmt = select(self.orm_model).where(self.orm_model.user_id == user_id)
        result = await self.session.execute(stmt)
        tokens = result.scalars().all()
        for t in tokens:
            await self.session.delete(t)
        await self.session.commit()
