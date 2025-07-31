from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.logger import DP_LOGGER

if TYPE_CHECKING:
    from bot.config import Config


def create_dispatcher(config: "Config") -> Dispatcher:
    logger = getLogger(DP_LOGGER)

    try:
        storage = MemoryStorage()

        dp = Dispatcher(storage=storage)
        dp["bot_start_time"] = datetime.now()
        logger.info("Dispatcher created")
    except Exception as e:
        logger.critical("Redis init error: %s", e, exc_info=True)
        raise e

    return dp
