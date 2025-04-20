from asyncio import current_task
from typing import TYPE_CHECKING, Any

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from storages.models import Base

if TYPE_CHECKING:
    from config import Config


class Engine:
    def __init__(self, config: "Config"):
        self._engine: AsyncEngine | None = None
        self.metadata: type[MetaData] = Base.metadata
        self.config = config.pg
        self.async_session_factory = None
        self._db: type[DeclarativeBase] = Base
        # self.session: async_sessionmaker[AsyncSession] | None = None

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        _ = self.engine

        self.async_session_factory = async_scoped_session(
            async_sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                autoflush=False,
                class_=AsyncSession
            ),
            scopefunc=current_task
        )
        # self.session = async_sessionmaker(
        #         bind=self.engine,
        #         expire_on_commit=False,
        #         autoflush=False,
        #         class_=AsyncSession
        #     )

        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._async_session_factory = None
            self._session_maker = None

    def _create_engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(
                url=self.config.database_url,
                # echo=True,
            )
        return self._engine
