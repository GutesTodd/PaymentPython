from fastapi import APIRouter

payment_router = APIRouter(prefix="payment", tags=["Платежи"])


@payment_router.post("/buy-subs")
async def buy_subscription(
    
)