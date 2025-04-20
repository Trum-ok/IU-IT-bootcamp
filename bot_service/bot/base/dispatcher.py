from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING

from aiogram import Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import ConnectionPool, Redis

from bot.logger import DP_LOGGER

if TYPE_CHECKING:
    from bot.config import Config


def create_dispatcher(config: "Config") -> Dispatcher:
    logger = getLogger(DP_LOGGER)

    try:
        redis_pool = ConnectionPool.from_url(config.redis.redis_url)
        redis = Redis(connection_pool=redis_pool)
        storage = RedisStorage(redis)

        dp = Dispatcher(storage=storage)
        dp["bot_start_time"] = datetime.now()
        logger.info("Dispatcher created")
    except Exception as e:
        logger.critical("Redis init error: %s", e, exc_info=True)
        raise e

    return dp


def setup_routers(dp: Dispatcher, routers: list[Router]) -> None:
    logger = getLogger(DP_LOGGER)

    dp.include_routers(*routers)
    logger.info(
        "Included routers: [%s]", ", ".join(router.name for router in routers)
    )
