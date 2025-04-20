from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from functools import wraps
from logging import getLogger
from typing import (
    TYPE_CHECKING,
    Any,
    ParamSpec,
    TypeVar,
)

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from app.web.app import Application

P = ParamSpec("P")
T = TypeVar("T")


class BaseAccessor:
    def __init__(self, app: "Application", *args, **kwargs):
        self.app = app
        self.logger = getLogger("accessor")

        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    @asynccontextmanager
    async def _session(self) -> AsyncIterator[AsyncSession]:
        if self.app.database.async_session_factory is None:
            raise RuntimeError("Database not connected")

        session: AsyncSession = self.app.database.async_session_factory()
        try:
            async with session.begin():
                yield session
        finally:
            await session.close()

    @classmethod
    def connection(
        cls, method: Callable[P, Coroutine[Any, Any, T]]
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(method)
        async def wrapper(
            self: "BaseAccessor", *args: P.args, **kwargs: P.kwargs
        ) -> T:
            async with self._session() as session:
                return await method(self, *args, **kwargs, session=session)

        return wrapper

    async def connect(self, app: "Application") -> None:
        return

    async def disconnect(self, app: "Application") -> None:
        return
