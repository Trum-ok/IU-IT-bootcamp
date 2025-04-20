import asyncio
import os

from bot.base.bot import run_bot

CONF_FILE = ".env"


def main(config_path: str) -> None:
    asyncio.run(run_bot(config_path))


if __name__ == "__main__":
    main(config_path=os.path.join(os.path.dirname(__file__), CONF_FILE))
