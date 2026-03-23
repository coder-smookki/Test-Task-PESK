import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers import start_router, help_router, search_router, city_query_router
from app.bot.callbacks import refresh_router
from app.bot.middlewares import ThrottlingMiddleware, LoggingMiddleware
from app.bot.utils.logging import setup_logger
from app.bot.utils.config import GREEN, RESET, BOLD, MAGENTA, DIM, CYAN
from app.services.http_client import close_client
from app.config import settings

logger = logging.getLogger("bot")


def create_bot() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    return bot, dp


bot, dp = create_bot()



def register_handlers(dispatcher: Dispatcher) -> None:
    routers = [
        ("start", start_router),
        ("help", help_router),
        ("search", search_router),
        ("city_query", city_query_router),
        ("ref>resh", refresh_router),
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
