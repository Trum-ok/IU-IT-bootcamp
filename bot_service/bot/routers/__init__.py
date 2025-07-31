from logging import getLogger

from aiogram import Dispatcher

from bot.logger import DP_LOGGER

from .main import main_router

__all__ = ("routers",)

routers = [main_router]


def setup_routers(dp: Dispatcher) -> None:
    logger = getLogger(DP_LOGGER)

    dp.include_routers(*routers)
    logger.info("Included routers: [%s]", ", ".join(router.name for router in routers))
