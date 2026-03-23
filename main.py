import asyncio
import logging

from aiogram import Dispatcher

from app.bot.create_bot import bot, dp
from app.bot.handlers import start_router, help_router, search_router, city_query_router
from app.bot.callbacks import refresh_router
from app.bot.middlewares import ThrottlingMiddleware, LoggingMiddleware
from app.bot.utils.logging import setup_logger
from app.bot.utils.config import GREEN, RESET, BOLD, MAGENTA, DIM, CYAN

logger = logging.getLogger("bot")


def register_handlers(dp: Dispatcher) -> None:
    routers = [
        ("start", start_router),
        ("help", help_router),
        ("search", search_router),
        ("city_query", city_query_router),
        ("refresh", refresh_router),
    ]
    for name, router in routers:
        dp.include_router(router)
        logger.info(f"  {GREEN}+{RESET} роутер {BOLD}{name}{RESET}")


def register_middleware(dp: Dispatcher) -> None:
    middlewares = [
        ("ThrottlingMiddleware", ThrottlingMiddleware()),
        ("LoggingMiddleware", LoggingMiddleware()),
    ]
    for name, mw in middlewares:
        dp.update.middleware(mw)
        logger.info(f"  {MAGENTA}+{RESET} мидлварь {BOLD}{name}{RESET}")


async def main() -> None:
    setup_logger()

    logger.info(f"{DIM}--- Регистрация мидлварей ---{RESET}")
    register_middleware(dp)

    logger.info(f"{DIM}--- Регистрация хендлеров ---{RESET}")
    register_handlers(dp)

    me = await bot.me()
    logger.info(
        f"{CYAN}{BOLD}@{me.username}{RESET} "
        f"{GREEN}стартовал!{RESET}"
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
