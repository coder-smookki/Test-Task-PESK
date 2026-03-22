from app.bot.handlers.start import router as start_router
from app.bot.handlers.help import router as help_router
from app.bot.handlers.search import router as search_router

__all__ = [
    "start_router",
    "search_router",
    "help_router",
]
