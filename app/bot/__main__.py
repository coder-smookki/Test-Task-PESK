import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.callbacks import refresh_router
from app.bot.handlers import city_query_router, help_router, search_router, start_router
from app.bot.middlewares import LoggingMiddleware, ThrottlingMiddleware
from app.bot.utils.config import BOLD, CYAN, DIM, GREEN, MAGENTA, RESET
from app.bot.utils.logging import setup_logger
from app.config import settings
from app.services.http_client import close_client

logger = logging.getLogger("bot")


def create_bot() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    return bot, dp


def register_handlers(dispatcher: Dispatcher) -> None:
    routers = [
        ("start", start_router),
        ("help", help_router),
        ("search", search_router),
        ("city_query", city_query_router),
        ("refresh", refresh_router),
    ]
    for name, router in routers:
        dispatcher.include_router(router)
        logger.info(f"  {GREEN}+{RESET} роутер {BOLD}{name}{RESET}")


def register_middleware(dispatcher: Dispatcher) -> None:
    middlewares = [
        ("ThrottlingMiddleware", ThrottlingMiddleware()),
        ("LoggingMiddleware", LoggingMiddleware()),
    ]
    for name, mw in middlewares:
        dispatcher.update.middleware(mw)
        logger.info(f"  {MAGENTA}+{RESET} мидлварь {BOLD}{name}{RESET}")


async def main() -> None:
    setup_logger()

    bot, dp = create_bot()

    logger.info(f"{DIM}--- Регистрация мидлварей ---{RESET}")
    register_middleware(dp)

    logger.info(f"{DIM}--- Регистрация хендлеров ---{RESET}")
    register_handlers(dp)

    me = await bot.me()
    logger.info(f"{CYAN}{BOLD}@{me.username}{RESET} {GREEN}стартовал!{RESET}")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await close_client()


if __name__ == "__main__":
    asyncio.run(main())
