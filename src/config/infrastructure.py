from pydantic import BaseModel
from pydantic_settings import BaseSettings

from .env import env

class CryptoBotSettings(BaseModel):
    TOKEN: str = env.str("CRYPTOBOT_TOKEN", "test")
    IS_TESTNET: bool = env.str("IS_TESTNET", True)
    
    
class InfrastructureSettings(BaseSettings):
    CRYPTO_BOT = CryptoBotSettings()
    
infrastructure_settings = InfrastructureSettings()