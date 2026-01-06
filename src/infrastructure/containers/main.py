from dependency_injector import containers, providers

from config.db import db_settings
from config.infrastructure import infrastructure_settings
from config.fastapi import fastapi_settings

from .core import CoreContainer
from .data import DataContainer
from .services import ServiceContainer

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.db.from_dict(db_settings.model_dump())
    config.infra.from_dict(infrastructure_settings.model_dump())
    config.fastapi.from_dict(fastapi_settings.model_dump())

    core = providers.Container(
        CoreContainer,
        db_url=config.db.async_url,
        crypto_token=config.infra.CRYPTO_BOT.TOKEN,
        is_testnet=config.infra.CRYPTO_BOT.IS_TESTNET,
    )

    data = providers.Container(
        DataContainer,
        session_factory=core.session_factory,
    )

    services = providers.Container(
        ServiceContainer,
        user_repo=data.user_repo,
        token_repo=data.token_repo,
        payment_repo=data.payment_repo,
        sub_repo=data.sub_repo,
        plan_repo=data.plan_repo,
        gateway=core.crypto_gateway,
        security_config=config.fastapi.SECURITY
    )