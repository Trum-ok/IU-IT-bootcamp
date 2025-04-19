from pathlib import Path
from typing import List
from uuid import uuid4
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine, update, select, delete

from .models import Base, Company, Publication, User, Subscriber, Subscription
from .config import CONTENT_AGREGATOR_DB 

from .base_database import Database
from .exceptions import UserExists, UserNotFound, CompanyNotFound

class ContentAgregatorDatabase(Database):
    def __init__(self):
        self.db_name = CONTENT_AGREGATOR_DB
        self.engine = create_async_engine(self.db_name, echo=False)
        self.SessionLocal =  async_sessionmaker(bind=self.engine, expire_on_commit=False)


    async def init_db(self):
        db_file = Path(self.db_name.split(':///')[-1])
        if not db_file.exists():
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)  


    async def add_subscription(self, telegram_id: str, company_id: str):
        pass


    async def remove_subscription(self, telegram_id: str, company_id: str):
        # subscriber = await self.get_subscriber(telegram_id)
        # if subscriber is None:
        #     raise UserNotFound
        
        # company = await self.get_company(company_id)
        # if company is None:
        #     raise CompanyNotFound
        
        # async with self.SessionLocal() as session:
        #     stmt = delete(Subscription).where(
        #         Subscription.subscriber_id.in_(
        #             select(Subscriber.id)
        #             .where(Subscriber.telegram_id == telegram_id)
        #             .scalar_subquery()
        #         )
        #     )
        #     result = await session.execute(stmt)
        pass


    async def get_company(self, id: str) -> Company | None:
        async with self.SessionLocal() as session:
            stmt = select(Company).where(Company.id == id)
            result = await session.execute(stmt)
            return result.scalar()
        

    async def get_companies(self) -> List[Company]:
        async with self.SessionLocal() as session:
            stmt = select(Company)
            result = await session.execute(stmt)
            return result.scalars()


    async def get_subscriber(self, id: str) -> Subscriber | None:
        async with self.SessionLocal() as session:
            stmt = select(Subscriber).where(Subscriber.id == id)
            result = await session.execute(stmt)
            return result.scalar()


    async def get_user_by_id(self, id: str) -> User | None:
        async with self.SessionLocal() as session:
            stmt = select(User).where(User.id == id)
            result = await session.execute(stmt)
            return result.scalar()


    async def get_user_by_login(self, login: str) -> User | None:
        async with self.SessionLocal() as session:
            stmt = select(User).where(User.login == login)
            result = await session.execute(stmt)
            return result.scalar()


    async def get_users(self) -> List[User]:
        async with self.SessionLocal() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            return result.scalars()


    async def add_user(self, login: str, password: str, role: str, company_id: str | None) -> None:
        user = await self.get_user_by_login(login)
        if user is not None:
            raise UserExists
        else:
            user_id = str(uuid4())
            async with self.SessionLocal() as session:
                user = User(id=user_id, 
                            login=login, 
                            password=password, 
                            role=role, 
                            company_id=company_id)
                session.add(user)
                await session.commit()


    async def remove_user(self, id: str) -> None:
        user = await self.get_user_by_id(id)
        if user is None:
            raise UserNotFound
        else:
            async with self.SessionLocal() as session:
                stmt = delete(User).where(User.id == id)
                await session.execute(stmt)
                await session.commit()


db = ContentAgregatorDatabase()

asyncio.run(db.init_db())
