import logging
import sys

from app.config import settings
from app.bot.utils.config import DIM, RESET, YELLOW, GREEN, BOLD, \
    RED, GREY, CYAN


LEVEL_STYLES = {
    logging.DEBUG: f"{DIM}DEBUG{RESET}",
    logging.INFO: f"{GREEN}INFO{RESET} ",
    logging.WARNING: f"{YELLOW}WARN{RESET} ",
    logging.ERROR: f"{RED}ERROR{RESET}",
    logging.CRITICAL: f"{BOLD}{RED}CRIT{RESET} ",
}


class PrettyFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ts = self.formatTime(record, "%H:%M:%S")
        level = LEVEL_STYLES.get(record.levelno, record.levelname)
        name = f"{DIM}{record.name}{RESET}"
        msg = record.getMessage()
        return f"{GREY}{ts}{RESET}  {level}  {name}  {msg}"


def setup_logger() -> logging.Logger:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(PrettyFormatter())
    root.handlers = [handler]

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

    logger = logging.getLogger("bot")
    logger.info(f"{CYAN}{BOLD}Бот запущен...{RESET}")
    return logger
