import asyncio
import logging
import signal
import sys
from typing import NoReturn

from aiogram import Bot, Dispatcher

from bot.base.defaults import DEFAULTS, Defaults
from bot.base.dispatcher import create_dispatcher, setup_routers
from bot.config import Config
from bot.logger import BOT_LOGGER, setup_logging
from bot.routers import routers


__all__ = (
    "ITSBot",
    "run_bot",
)


class ITSBot(Bot):
    def __init__(self, token: str, defaults: Defaults, ports: "Ports"):
        super().__init__(token=token, default=defaults)
        self.ports = ports
        self.logger = logging.getLogger(BOT_LOGGER)


async def graceful_shutdown(bot: "ITSBot", dp: Dispatcher) -> None:
    bot.logger.warning("Starting graceful shutdown...")

    await bot.delete_webhook(drop_pending_updates=False)

    if hasattr(dp, "storage") and dp.storage:
        await dp.storage.redis.close()
        bot.logger.info("Storage closed")

    if bot.session:
        await bot.session.close()
        bot.logger.info("Session closed")

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)

    bot.logger.warning("Shutdown complete!")


def register_shutdown_handlers(bot: Bot, dp: Dispatcher) -> None:
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda: asyncio.create_task(graceful_shutdown(bot, dp))
        )


async def run_bot(config_path: str) -> ITSBot:
    setup_logging()

    config = Config(config_path)
    ports = Ports(config)

    bot = ITSBot(token=config.tg.token, defaults=DEFAULTS, ports=ports)
    dp: Dispatcher = create_dispatcher(config)

    setup_routers(dp, routers)

    register_shutdown_handlers(bot, dp)

    bot.logger.info("Starting bot...")

    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        bot.logger.critical("Unexpected error: %s", e, exc_info=True)
    finally:
        if bot.session:
            await graceful_shutdown(bot, dp)
