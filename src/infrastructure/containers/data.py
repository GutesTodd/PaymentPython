from dependency_injector import containers, providers
from src.infrastructure.db.repositories.user import UserRepository
from src.infrastructure.db.repositories.refresh_token import RefreshTokenRepository
from src.infrastructure.db.repositories.payment import PaymentRepository
from src.infrastructure.db.repositories.subscription import SubscriptionRepository
from src.infrastructure.db.repositories.plan import PlanRepository

class DataContainer(containers.DeclarativeContainer):
    session_factory = providers.Dependency()

    db_session = providers.Factory(
        lambda factory: factory(),
        factory=session_factory
    )

    user_repo = providers.Factory(UserRepository, session=db_session)
    token_repo = providers.Factory(RefreshTokenRepository, session=db_session)
    payment_repo = providers.Factory(PaymentRepository, session=db_session)
    sub_repo = providers.Factory(SubscriptionRepository, session=db_session)
    plan_repo = providers.Factory(PlanRepository, session=db_session)