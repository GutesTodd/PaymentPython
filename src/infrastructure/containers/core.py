from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from infrastructure.cryptobot.client import CryptoBotClient

class CoreContainer(containers.DeclarativeContainer):
    db_url = providers.Dependency()
    crypto_token = providers.Dependency()
    is_testnet = providers.Dependency()

    engine = providers.Singleton(create_async_engine, url=db_url)

    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    crypto_gateway = providers.Singleton(
        CryptoBotClient,
        token=crypto_token,
        is_testnet=is_testnet,
    )