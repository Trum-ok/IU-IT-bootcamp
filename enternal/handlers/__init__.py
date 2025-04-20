from typing import TYPE_CHECKING

from handlers.main import main_router

if TYPE_CHECKING:
    from fastapi import FastAPI

routers = [main_router,]


def setup_routers(app: "FastAPI"):
    for router in routers:
        app.include_router(router)
