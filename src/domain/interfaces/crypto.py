from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TypedDict

class InvoiceData(TypedDict):
    invoice_id: int
    pay_url: str

class IPaymentGateway(ABC):
    @abstractmethod
    async def create_invoice(self, amount: Decimal, asset: str) -> InvoiceData:
        pass

    @abstractmethod
    def verify_webhook_signature(self, body: str, signature: str) -> bool:
        pass