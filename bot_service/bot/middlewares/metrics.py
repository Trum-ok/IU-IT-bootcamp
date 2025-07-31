from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, types


class MetricsMiddleware(BaseMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.lock = asyncio.Lock()
        # self.total_time = 0.0
        # self.total_requests = 0
        # self.timestamps = []
        # self.metrics_history = {'time': [], 'rps': []}

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        pass


#         start_time = time.monotonic()
#         try:
#             return await handler(event, data)
#         finally:
#             duration = time.monotonic() - start_time

#             async with self.lock:
#                 # Update average time metrics
#                 self.total_time += duration
#                 self.total_requests += 1

#                 # Update RPS metrics
#                 now = time.time()
#                 self.timestamps.append(now)

#                 # Remove old timestamps (older than 1 second)
#                 cutoff = now - 1.0
#                 while self.timestamps and self.timestamps[0] < cutoff:
#                     self.timestamps.pop(0)

#     def get_metrics(self):
#         """Return current metrics"""
#         async def _get():
#             async with self.lock:
#                 avg_time = self.total_time / self.total_requests
#                 if self.total_requests else 0
#                 rps = len(self.timestamps)
#                 return {
#                     'avg_time': avg_time,
#                     'rps': rps
#                 }
#         return _get()

#     async def update_history(self):
#         """Update metrics history for graphing"""
#         async with self.lock:
#             metrics = await self.get_metrics()
#             self.metrics_history['time'].append(metrics['avg_time'])
#             self.metrics_history['rps'].append(metrics['rps'])

#             # Keep last 60 data points (5 minutes if updated every 5 seconds)
#             for key in self.metrics_history:
#                 if len(self.metrics_history[key]) > 60:
#                     self.metrics_history[key].pop(0)


# bot = Bot(token="YOUR_BOT_TOKEN")
# dp = Dispatcher()
# metrics_middleware = MetricsMiddleware()

# dp.message.middleware(metrics_middleware)


# @dp.startup()
# async def on_startup():
#     # Запуск фоновой задачи для графиков
#     asyncio.create_task(metrics_graph_task(metrics_middleware))


# @dp.message(commands=["metrics"])
# async def send_metrics(message: types.Message):
#     """Send metrics data and graph to user"""
#     metrics = await metrics_middleware.get_metrics()

#     text = (
#         "📊 Bot Metrics:\n"
#         f"• Avg processing time: {metrics['avg_time']:.3f}s\n"
#         f"• Current RPS: {metrics['rps']}"
#     )

#     with open('metrics.png', 'rb') as photo:
#         await message.answer_photo(photo, caption=text)
