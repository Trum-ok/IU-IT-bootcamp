import logging
import sys

ACCESSOR_LOGGER = "accessor"

LOGGERS = [ACCESSOR_LOGGER]

STANDART_FORMAT = "%(asctime)s | %(name)-20s - %(levelname)s - %(message)s"
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=STANDART_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(),
        # RotatingFileHandler(  # TODO: расскоментировать перед релизом
        #     "bot.log",
        #     maxBytes=5*1024*1024
        #     backupCount=3
        # )
    ],
)


def setup_logging() -> None:
    standard_formatter = logging.Formatter(STANDART_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(standard_formatter)
    console_handler.setLevel(logging.INFO)

    for logger_name in LOGGERS:
        logger = logging.getLogger(logger_name)
        logger.addHandler(console_handler)
        # logger.addHandler(error_handler)
        logger.propagate = False
