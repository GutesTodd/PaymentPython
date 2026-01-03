from pydantic_settings import BaseSettings

from .env import env


class DatabaseSettings(BaseSettings):
    DB_USER: str = env.str('DB_USER', 'postgres')
    DB_PASSWORD: str = env.str('DB_PASSWORD', 'postgres')
    DB_HOST: str = env.str('DB_HOST', '127.0.0.1')
    DB_PORT: int = env.int('DB_PORT', 5432)
    DB_NAME: str = env.str('DB_NAME', 'payment_backend')

    @property
    def async_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def sync_url(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


db_settings = DatabaseSettings()
