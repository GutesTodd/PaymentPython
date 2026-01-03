from sqlalchemy import select
from src.domain.entities import Payment, PaymentStatus
from src.domain.interfaces.repositories import IPaymentRepository
from src.infrastructure.db.models.payment import PaymentORM
from .base import BaseRepository

class PaymentRepository(BaseRepository[PaymentORM], IPaymentRepository):
    async def get_by_external_id(self, external_id: int) -> Payment | None:
        stmt = select(self.orm_model).where(self.orm_model.external_id == external_id)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()
        
        if not obj:
            return None
        return Payment(
            id=str(obj.id),
            user_id=obj.user_id,
            plan_id=obj.plan_id,
            amount=obj.amount,
            external_id=obj.external_id,
            status=PaymentStatus(obj.status),
            pay_url=obj.pay_url,
            created_at=obj.created_at
        )

    async def save(self, payment: Payment) -> Payment:
        orm_obj = PaymentORM(
            external_id=payment.external_id,
            user_id=payment.user_id,
            plan_id=payment.plan_id,
            amount=payment.amount,
            status=payment.status.value,
            pay_url=payment.pay_url
        )
        await self.add(orm_obj)
        payment.id = str(orm_obj.id)
        return payment