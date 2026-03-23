from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from app.bot.keyboards.start import start_keyboard
from app.bot.utils.config import START_TEXT
from app.bot.utils.photo_cache import get_photo, save_photo_id

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    result = await message.answer_photo(
        photo=get_photo("start"),
        caption=START_TEXT,
        reply_markup=start_keyboard(),
    )
    save_photo_id("start", result)


@router.callback_query(F.data.in_({"cancel", "view_menu"}))
async def on_back_to_menu(callback: CallbackQuery) -> None:
    if callback.message.photo:
        result = await callback.message.edit_media(
            media=InputMediaPhoto(
                media=get_photo("start"),
                caption=START_TEXT,
            ),
            reply_markup=start_keyboard(),
        )
    else:
        await callback.message.delete()
        result = await callback.message.answer_photo(
            photo=get_photo("start"),
            caption=START_TEXT,
            reply_markup=start_keyboard(),
        )
    save_photo_id("start", result)
    await callback.answer()
