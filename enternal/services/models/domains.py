from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DomainEntity(BaseModel):
    """Базовый класс для всех доменных сущностей"""

    id: str


class ValueObject(BaseModel):
    """Базовый класс для Value Objects"""


class User(DomainEntity):
    login: str
    password_hash: str
    role: str
    company: Optional["Company"] = None
    publications: list["Publication"] = []

    def has_permission(self, required_role: str) -> bool:
        return self.role == required_role

    def change_password(self, new_hash: str) -> None:
        self.password_hash = new_hash


class Company(DomainEntity):
    name: str
    description: str
    image_url: str
    authors: list["User"] = []
    subscriptions: list["Subscription"] = []

    def add_author(self, user: User) -> None:
        if user not in self.authors:
            self.authors.append(user)
            user.company = self

    def remove_author(self, user: User) -> None:
        if user in self.authors:
            self.authors.remove(user)
            user.company = None


class Publication(DomainEntity):
    title: str
    content: str
    main_image_url: str
    created_at: datetime
    author: str  # TODO в сервисе подтянуть юзера

    def can_edit(self, user: "User") -> bool:
        return user == self.author or user.has_permission("admin")


class Subscriber(DomainEntity):
    telegram_id: str
    subscriptions: list["Subscription"] = []

    def subscribe_to(self, company: "Company") -> None:
        if not any(sub.company == company for sub in self.subscriptions):
            self.subscriptions.append(
                Subscription(subscriber=self, company=company)
            )

    def unsubscribe_from(self, company: "Company") -> None:
        self.subscriptions = [
            sub for sub in self.subscriptions if sub.company != company
        ]


class Subscription(DomainEntity):
    subscriber: "Subscriber"
    company: "Company"
