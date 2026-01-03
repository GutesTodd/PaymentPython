from pydantic import BaseModel
from decimal import Decimal

class CryptoBotInvoiceResult(BaseModel):
    invoice_id: int
    pay_url: str
    amount: Decimal
    asset: str
    status: str

class CryptoBotResponse(BaseModel):
    ok: bool
    result: CryptoBotInvoiceResult