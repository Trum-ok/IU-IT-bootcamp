from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    """Default class for tables"""

    __abstract__ = True


class Publication(Base):
    __tablename__ = "Publications"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    main_image_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    # Foreign keys
    author_id: Mapped[str] = mapped_column(String, ForeignKey("Users.id"))

    # Relationships
    author: Mapped["User"] = relationship(back_populates="publications")


class Company(Base):
    __tablename__ = "Companies"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)

    # Relationships
    authors: Mapped[list["User"]] = relationship(back_populates="company")
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="company"
    )


class User(Base):
    __tablename__ = "Users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    login: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    company_id: Mapped[str] = mapped_column(
        String, ForeignKey("Companies.id"), nullable=True
    )

    # Relationships
    company: Mapped["Company"] = relationship(back_populates="authors")
    publications: Mapped["Publication"] = relationship(back_populates="author")


class Subscriber(Base):
    __tablename__ = "Subscribers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[str] = mapped_column(String)

    # Relationships
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="subscriber"
    )


class Subscription(Base):
    __tablename__ = "Subscriptions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subscriber_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("Subscribers.id")
    )
    company_id: Mapped[str] = mapped_column(String, ForeignKey("Companies.id"))

    # Relationships
    subscriber: Mapped["Subscriber"] = relationship(
        back_populates="subscriptions"
    )
    company: Mapped["Company"] = relationship(back_populates="subscriptions")
