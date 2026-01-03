from sqlalchemy import select

from infrastructure.db.models.payment import PaymentORM
from infrastructure.db.mapper import Mapper
from domain.entities import Payment

class PaymentRepository(BaseRepository[PaymentORM, Payment]):
    async def get_by_external_id(self, external_id: int) -> Payment | None:
        stmt = select(self.orm_model).where(self.orm_model.external_id == external_id)
        result = await self.session.execute(stmt)
        orm_obj = result.scalars().first()
        return Mapper.to_domain(orm_obj, self.entity_model)