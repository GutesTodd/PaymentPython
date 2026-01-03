from pydantic_settings import BaseSettings

from infrastructure.config.security import SecurityConfig

from .env import env


class FastAPISettings(BaseSettings):
    ROOT_PATH: str = '/backend'
    DEBUG: bool = env.bool('DEBUG', True)
    CORS_ALLOWED_ORIGINS: list[str] = env.list('CORS_ALLOWED_ORIGINS', ['*'])
    WORKERS: int = 4

    SECURITY: SecurityConfig = SecurityConfig(
        SECRET_KEY=env.str('SECRET_KEY', 'secret'),
        ALGORITHM=env.str('ALGORITHM', 'HS256'),
        ACCESS_EXP_MINUTES=env.int('ACCESS_TOKEN_EXPIRE_MINUTES', 60),
        REFRESH_EXP_DAYS=env.int('REFRESH_TOKEN_EXPIRE_DAYS', 30),
    )


fastapi_settings = FastAPISettings()
