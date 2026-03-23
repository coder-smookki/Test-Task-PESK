import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot.utils.logging import setup_logger
from app.bot.utils.config import BLUE, BOLD, GREEN, RESET
from app.api.router import router as api_router
from app.services.http_client import close_client

logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await close_client()


app = FastAPI(title="Test Task Pesk API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


if __name__ == "__main__":
    setup_logger()
    logger.info(f"{BLUE}{BOLD}АПИ{RESET} {GREEN}запущен на http://0.0.0.0:8000{RESET}")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
