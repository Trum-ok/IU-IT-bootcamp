from aiogram import Dispatcher

from .metrics import MetricsMiddleware

message_middlewares = [
    MetricsMiddleware,
]


def setup_middlewares(dp: Dispatcher):
    for m in message_middlewares:
        dp.message.middleware(m)
