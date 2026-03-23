import time
import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

logger = logging.getLogger("bot.updates")

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[38;5;117m"
MAGENTA = "\033[38;5;176m"
YELLOW = "\033[38;5;221m"
GREEN = "\033[38;5;114m"
BLUE = "\033[38;5;75m"


def _user_tag(user) -> str:
    name = user.full_name or "Unknown"
    return f"{BOLD}{name}{RESET} {DIM}[{user.id}]{RESET}"


def _describe(event: TelegramObject, data: Dict[str, Any]) -> str:
    if isinstance(event, Message):
        if event.text and event.text.startswith("/"):
            cmd = event.text.split()[0]
            return f"{CYAN}command{RESET}  {BOLD}{cmd}{RESET}"
        if event.text:
            preview = event.text[:40] + ("..." if len(event.text) > 40 else "")
            return f"{BLUE}text{RESET}     {preview}"
        return f"{DIM}message{RESET}  {event.content_type}"

    if isinstance(event, CallbackQuery):
        return f"{MAGENTA}callback{RESET} {BOLD}{event.data}{RESET}"

    return f"{DIM}{type(event).__name__}{RESET}"


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        tag = _user_tag(user)
        desc = _describe(event, data)
        logger.info(f"{tag}  {desc}")

        start = time.monotonic()
        result = await handler(event, data)
        ms = (time.monotonic() - start) * 1000

        color = GREEN if ms < 500 else YELLOW
        logger.info(f"{tag}  {GREEN}done{RESET} {color}{ms:.0f}ms{RESET}")
        return result
