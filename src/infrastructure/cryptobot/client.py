import hashlib
import hmac
from decimal import Decimal
from typing import Any, Dict

import httpx
from domain.interfaces.crypto import IPaymentGateway, InvoiceData
from infrastructure.cryptobot.dto import CryptoBotResponse

class CryptoBotClient(IPaymentGateway):
    def __init__(self, token: str, is_testnet: bool = True):
        self._token = token
        self._base_url = (
            "https://testnet-pay.crypt.bot/api" if is_testnet 
            else "https://pay.crypt.bot/api"
        )
        self._headers = {
            "Crypto-Pay-API-Token": self._token,
            "Content-Type": "application/json"
        }

    async def create_invoice(self, amount: Decimal, asset: str) -> InvoiceData:
        url = f"{self._base_url}/createInvoice"
        payload = {
            "amount": str(amount),
            "asset": asset
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url, 
                json=payload, 
                headers=self._headers
            )
            response.raise_for_status() 
            
            data = CryptoBotResponse.model_validate(response.json())
            
            if not data.ok:
                raise Exception("CryptoBot API returned not ok")

            return {
                "invoice_id": data.result.invoice_id,
                "pay_url": data.result.pay_url
            }

    def verify_webhook_signature(self, body: str, signature: str) -> bool:
        secret = hashlib.sha256(self._token.encode()).digest()
        
        hmac_check = hmac.new(
            secret, 
            body.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(hmac_check, signature)