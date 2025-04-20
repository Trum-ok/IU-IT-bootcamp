import logging
import sys

from logging.handlers import RotatingFileHandler

BOT_LOGGER = "bot"
DP_LOGGER = "aiogram.dispatcher"
EVENT_LOGGER = "bot.event"
MW_LOGGER = "bot.middlewares"
WH_LOGGER = "bot.webhook"

LOGGERS = [
    BOT_LOGGER,
    DP_LOGGER,
    EVENT_LOGGER,
    MW_LOGGER,
    WH_LOGGER,
]

STANDART_FORMAT = "%(asctime)s | %(name)-20s - %(levelname)s - %(message)s"
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"


logging.basicConfig(
    level=logging.INFO,
    format=STANDART_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            "bot.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
        ),
    ],
)


def setup_logging() -> None:  # TODO
    main_logger = logging.getLogger(BOT_LOGGER)
    main_logger.setLevel(logging.INFO)

    standard_formatter = logging.Formatter(STANDART_FORMAT, datefmt=DATE_FORMAT)
    # error_formatter = logging.Formatter(
    #     "%(asctime)s | %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",  # noqa: E501
    #     datefmt="%d-%m-%Y %H:%M:%S",
    # )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(standard_formatter)
    console_handler.setLevel(logging.INFO)

    # error_handler = logging.StreamHandler(sys.stderr)
    # error_handler.setFormatter(error_formatter)
    # error_handler.setLevel(logging.WARNING)

    for logger_name in LOGGERS:
        logger = logging.getLogger(logger_name)
        logger.addHandler(console_handler)
        # logger.addHandler(error_handler)
        logger.propagate = False
