import json
from domain.entities import Payment, PaymentStatus
from domain.exceptions import UserBannedException
from domain.interfaces.crypto import IPaymentGateway
from infrastructure.db.repositories.payment import PaymentRepository
from infrastructure.db.repositories.user import UserRepository
from infrastructure.db.repositories.subscription import SubscriptionRepository
from infrastructure.db.repositories.plan import PlanRepository

class PaymentService:
    def __init__(
        self,
        payment_repo: PaymentRepository,
        user_repo: UserRepository,
        sub_repo: SubscriptionRepository,
        plan_repo: PlanRepository,
        gateway: IPaymentGateway
    ):
        self.payment_repo = payment_repo
        self.user_repo = user_repo
        self.sub_repo = sub_repo
        self.plan_repo = plan_repo
        self.gateway = gateway

    async def buy_subscription_by_telegram(self, tg_id: int, plan_id: str) -> Payment:
        user = await self.user_repo.get_by_tg_id(tg_id)
        if not user:
            raise ValueError("Пользователя с таким Telegram ID не существует")

        plan = await self.plan_repo.get_by_id(plan_id)
        
        if user.is_banned:
            raise UserBannedException("Пользователь забанен")

        invoice = await self.gateway.create_invoice(plan.price, "USDT")

        new_payment = Payment(
            id=None,
            user_id=user.id,
            plan_id=plan.id,
            amount=plan.price,
            external_id=invoice["invoice_id"],
            pay_url=invoice["pay_url"],
            status=PaymentStatus.PENDING
        )
        return await self.payment_repo.add(new_payment)

    async def process_webhook(self, body_str: str, signature: str):
        if not self.gateway.verify_webhook_signature(body_str, signature):
            raise Exception("Некорректная подпись")

        payload = json.loads(body_str).get("payload", {})
        if payload.get("status") != "paid":
            return

        payment = await self.payment_repo.get_by_external_id(payload["invoice_id"])
        if not payment or payment.status == PaymentStatus.PAID:
            return

        user = await self.user_repo.get(payment.user_id)
        current_sub = await self.sub_repo.get_by_user_id(user.id)
        plan = await self.plan_repo.get_by_id(payment.plan_id)

        new_sub = user.extend_subscription(current_sub, plan)
        payment.mark_as_paid()

        await self.payment_repo.update(payment)
        await self.sub_repo.save_subscription(new_sub)