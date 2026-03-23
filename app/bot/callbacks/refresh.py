from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto

from app.bot.keyboards.result import result_keyboard, RefreshCallback
from app.bot.utils.config import REFRESH_DONE, REFRESH_NO_CHANGE, REFRESH_FAIL
from app.bot.utils.formatters import format_result
from app.bot.utils.photo_cache import get_photo, save_photo_id
from app.services.city_info import get_city_info

router = Router()


@router.callback_query(RefreshCallback.filter())
async def on_refresh(callback: CallbackQuery, callback_data: RefreshCallback) -> None:
    city = callback_data.city
    amount = callback_data.amount

    data = await get_city_info(city, amount, force=True)
    if data is None:
        await callback.answer(REFRESH_FAIL, show_alert=True)
        return

    try:
        result = await callback.message.edit_media(
            media=InputMediaPhoto(
                media=get_photo("result"),
                caption=format_result(data),
            ),
            reply_markup=result_keyboard(city, amount),
        )
        save_photo_id("result", result)
        await callback.answer(REFRESH_DONE)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer(REFRESH_NO_CHANGE)
        else:
            raise
