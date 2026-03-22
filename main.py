import asyncio
import logging

from aiogram import Dispatcher

from app.bot.create_bot import bot, dp

from app.config import settings


def register_handlers(dp: Dispatcher) -> None:
    from app.bot.handlers import start_router
    from app.bot.handlers import help_router
    from app.bot.handlers import search_router

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(search_router)

def register_middleware(dp: Dispatcher) -> None:
    from app.bot.middlewares import ThrottlingMiddleware

    dp.update.middleware(ThrottlingMiddleware())


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    register_middleware(dp)
    register_handlers(dp)
    logging.info("Бот запущен https://t.me/test_smokkkiii_bot")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
