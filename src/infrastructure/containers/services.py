from dependency_injector import containers, providers
from src.services.user_service import UserService
from src.services.payment_service import PaymentService

class ServiceContainer(containers.DeclarativeContainer):
    user_repo = providers.Dependency()
    token_repo = providers.Dependency()
    payment_repo = providers.Dependency()
    sub_repo = providers.Dependency()
    plan_repo = providers.Dependency()
    gateway = providers.Dependency()
    security_config = providers.Dependency()

    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
        token_repo=token_repo,
        config=security_config,
    )

    payment_service = providers.Factory(
        PaymentService,
        payment_repo=payment_repo,
        user_repo=user_repo,
        sub_repo=sub_repo,
        plan_repo=plan_repo,
        gateway=gateway,
    )