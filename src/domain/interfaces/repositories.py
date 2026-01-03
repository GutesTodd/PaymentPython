from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import User, Subscription, Payment, SubscriptionPlan

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> Optional[User]: ...
    @abstractmethod
    async def save(self, user: User) -> User: ...

class ISubscriptionRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[Subscription]: ...
    @abstractmethod
    async def save(self, subscription: Subscription) -> Subscription: ...

class IPaymentRepository(ABC):
    @abstractmethod
    async def get_by_external_id(self, external_id: int) -> Optional[Payment]: ...
    @abstractmethod
    async def save(self, payment: Payment) -> Payment: ...

class IPlanRepository(ABC):
    @abstractmethod
    async def get_all_active(self) -> List[SubscriptionPlan]: ...
    @abstractmethod
    async def get_by_id(self, plan_id: str) -> Optional[SubscriptionPlan]: ...