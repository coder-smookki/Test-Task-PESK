from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from app.bot.keyboards.help import help_keyboard
from app.bot.utils.config import HELP_TEXT
from app.bot.utils.photo_cache import get_photo, save_photo_id

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    result = await message.answer_photo(
        photo=get_photo("help"),
        caption=HELP_TEXT,
        reply_markup=help_keyboard(),
    )
    save_photo_id("help", result)


@router.callback_query(F.data == "help")
async def on_help(callback: CallbackQuery) -> None:
    result = await callback.message.edit_media(
        media=InputMediaPhoto(
            media=get_photo("help"),
            caption=HELP_TEXT,
        ),
        reply_markup=help_keyboard(),
    )
    save_photo_id("help", result)
    await callback.answer()
