import time
import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.bot.utils.config import RESET, BOLD, DIM, RED, THROTTLE_RATE

logger = logging.getLogger("bot.throttle")


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
            logger.warning(
                f"{RED}throttled{RESET} {BOLD}{user.full_name}{RESET} "
                f"{DIM}[{user.id}]{RESET}"
            )
            return None

        self._cache[user.id] = now
        return await handler(event, data)
