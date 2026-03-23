import asyncio
import logging

import uvicorn
from aiogram import Dispatcher
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot.create_bot import bot, dp
from app.bot.handlers import start_router, help_router, search_router, city_query_router
from app.bot.callbacks import refresh_router
from app.bot.middlewares import ThrottlingMiddleware, LoggingMiddleware
from app.bot.utils.logging import setup_logger
from app.bot.utils.config import GREEN, RESET, BOLD, MAGENTA, DIM, CYAN, BLUE
from app.api.router import router as api_router
from app.services.http_client import close_client

logger = logging.getLogger("bot")

app = FastAPI(title="Тест-Таск-ПЭСК", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


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

    logger.info(f"{DIM}--- Регистрация мидлварей ---{RESET}")
    register_middleware(dp)

    logger.info(f"{DIM}--- Регистрация хендлеров ---{RESET}")
    register_handlers(dp)

    me = await bot.me()
    logger.info(
        f"{CYAN}{BOLD}@{me.username}{RESET} "
        f"{GREEN}стартовал!{RESET}"
    )

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    logger.info(
        f"{BLUE}{BOLD}АПИ{RESET} "
        f"{GREEN}запущен на http://127.0.0.1:8000{RESET}"
    )

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(
            dp.start_polling(bot),
            server.serve(),
        )
    finally:
        await close_client()


if __name__ == "__main__":
    asyncio.run(main())
