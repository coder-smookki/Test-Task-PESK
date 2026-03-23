import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import router as api_router
from app.api.web import router as web_router
from app.bot.utils.config import BLUE, BOLD, GREEN, RESET
from app.bot.utils.logging import setup_logger
from app.services.http_client import close_client

logger = logging.getLogger("api")

_ROOT = Path(__file__).resolve().parent.parent.parent


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await close_client()


app = FastAPI(
    title="Test Task Pesk API",
    version="1.0.0",
    description=(
        "REST API для получения информации о городе: "
        "геолокация, текущая погода (OpenWeatherMap) и конвертация валюты (ExchangeRate-API). "
        "Результаты кешируются на 5 минут."
    ),
    contact={"name": "АО ПЭСК"},
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(_ROOT / "app" / "static")), name="static")
app.include_router(api_router)
app.include_router(web_router)


if __name__ == "__main__":
    setup_logger()
    logger.info(f"{BLUE}{BOLD}АПИ{RESET} {GREEN}запущен на http://0.0.0.0:8000{RESET}")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
