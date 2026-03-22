import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

THROTTLE_RATE = 1.0


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate: float = THROTTLE_RATE) -> None:
        self._rate = rate
        self._cache: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        last = self._cache.get(user.id, 0.0)

        if now - last < self._rate:
            return None

        self._cache[user.id] = now
        return await handler(event, data)
