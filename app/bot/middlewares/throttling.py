import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.bot.utils.config import BOLD, DIM, RED, RESET, THROTTLE_RATE

logger = logging.getLogger("bot.throttle")

_MAX_CACHE_SIZE = 10_000


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate: float = THROTTLE_RATE) -> None:
        self._rate = rate
        self._cache: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        last = self._cache.get(user.id, 0.0)

        if now - last < self._rate:
            logger.warning(f"{RED}ТРОТТЛИНГ{RESET} {BOLD}{user.full_name}{RESET} " f"{DIM}[{user.id}]{RESET}")
            return None

        self._cache[user.id] = now

        if len(self._cache) > _MAX_CACHE_SIZE:
            oldest = sorted(self._cache, key=self._cache.__getitem__)
            for k in oldest[: len(self._cache) // 4]:
                del self._cache[k]

        return await handler(event, data)
