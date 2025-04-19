from pathlib import Path
from typing import List
from uuid import uuid4
from datetime import datetime
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, delete

from .models import Base, Company, Publication, User
from .config import CONTENT_AGREGATOR_DB

from .storage import Database
from .exceptions import UserExists, UserNotFound, PublicationNotFound


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


    async def get_publication(self, publication_id: str) -> Publication | None:
        async with self.SessionLocal() as session:
            stmt = select(Publication).where(Publication.id == publication_id)
            result = await session.execute(stmt)
            return result.scalar()


    async def get_publications(self) -> List[Publication]:
        async with self.SessionLocal() as session:
            stmt = select(Publication)
            result = await session.execute(stmt)
            return result.scalars()


    async def remove_publication(self, publication_id: str) -> None:
        publication = await self.get_publication(publication_id)
        if publication is None:
            raise PublicationNotFound
        else:
            async with self.SessionLocal() as session:
                stmt = delete(Publication).where(Publication.id == publication_id)
                await session.execute(stmt)
                await session.commit()


    async def add_publication(self, title: str, content: str, image_url: str, created_at: datetime, author_id: str) -> None:
        publication_id = str(uuid4())
        async with self.SessionLocal() as session:
            publication = Publication(
                id=publication_id,
                title=title,
                content=content,
                main_image_url=image_url,
                created_at=created_at,
                author_id=author_id
            )
            session.add(publication)
            await session.commit()


    async def update_publication(self, publication_id: str, title: str, content: str, image_url: str, created_at: datetime, author_id: str) -> None:
        publication = await self.get_publication(publication_id)
        if publication is None:
            raise PublicationNotFound
        else:
            async with self.SessionLocal() as session:
                publication.title = title
                publication.content = content
                publication.main_image_url = image_url
                publication.created_at = created_at
                publication.author_id = author_id

                session.add(publication)
                await session.commit()


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
                user = User(
                    id=user_id,
                    login=login,
                    password=password,
                    role=role,
                    company_id=company_id
                )
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
