from abc import ABC, abstractmethod
from datetime import datetime

from storages.models import (
    Company,
    Publication,
    Subscriber,
    Subscription,
    User,
)


class Database(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def init_db(self) -> None:
        pass

    @abstractmethod
    async def get_publication(self, publication_id: str) -> Publication | None:
        pass

    @abstractmethod
    async def get_publications(self) -> list[Publication]:
        pass

    @abstractmethod
    async def remove_publication(self, publication_id: str) -> None:
        pass

    @abstractmethod
    async def add_publication(
        self,
        title: str,
        content: str,
        image_url: str,
        created_at: datetime,
        author_id: str,
    ) -> None:
        pass

    @abstractmethod
    async def update_publication(
        self,
        publication_id: str,
        title: str,
        content: str,
        image_url: str,
        created_at: datetime,
        author_id: str,
    ) -> None:
        pass

    @abstractmethod
    async def get_company(self, id: str) -> Company | None:
        pass

    @abstractmethod
    async def get_companies(self) -> list[Company]:
        pass

    @abstractmethod
    async def get_user_by_id(self, id: str) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User | None:
        pass

    @abstractmethod
    async def get_users(self) -> list[User]:
        pass

    @abstractmethod
    async def add_user(
        self, login: str, password: str, role: str, company_id: str | None
    ) -> None:
        pass

    @abstractmethod
    async def remove_user(self, id: str) -> None:
        pass

    @abstractmethod
    async def get_subscriber_by_id(self, id: str) -> Subscriber:
        pass

    @abstractmethod
    async def get_subscriber_by_telegram_id(
        self, telegram_id: str
    ) -> Subscriber:
        pass

    @abstractmethod
    async def get_subscription_by_id(self, id: str) -> Subscription:
        pass
