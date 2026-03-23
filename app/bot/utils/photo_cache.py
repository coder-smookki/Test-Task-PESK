from aiogram.types import FSInputFile, Message

from app.bot.utils.config import PHOTO_PATHS

_cache: dict[str, str] = {}


def get_photo(name: str) -> str | FSInputFile:
    if name in _cache:
        return _cache[name]
    return FSInputFile(PHOTO_PATHS[name])


def save_photo_id(name: str, msg: Message) -> None:
    if msg.photo:
        _cache[name] = msg.photo[-1].file_id
 