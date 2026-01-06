from domain.entities import Subscription, SubscriptionPlan
from infrastructure.db.repositories.subscription import SubscriptionPlanRepository, SubscriptionRepository

class SubscriptionService:
    def __init__(
        self,
        sub_repo: SubscriptionRepository,
        sub_plan_repo: SubscriptionPlanRepository
    ):
        self._sub_repo = sub_repo
        self._sub_repo_plan = sub_plan_repo