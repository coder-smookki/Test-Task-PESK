from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from app.bot.keyboards.search import search_keyboard
from app.bot.utils.config import SEARCH_TEXT
from app.bot.utils.photo_cache import get_photo, save_photo_id

router = Router()


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    result = await message.answer_photo(
        photo=get_photo("search"),
        caption=SEARCH_TEXT,
        reply_markup=search_keyboard(),
    )
    save_photo_id("search", result)


@router.callback_query(F.data == "search")
async def on_search(callback: CallbackQuery) -> None:
    result = await callback.message.edit_media(
        media=InputMediaPhoto(
            media=get_photo("search"),
            caption=SEARCH_TEXT,
        ),
        reply_markup=search_keyboard(),
    )
    save_photo_id("search", result)
    await callback.answer()
