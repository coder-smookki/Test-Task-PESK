from aiogram import Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.result import result_keyboard, RefreshCallback

router = Router()


@router.callback_query(RefreshCallback.filter())
async def on_refresh(callback: CallbackQuery, callback_data: RefreshCallback) -> None:
    city = callback_data.city
    amount = callback_data.amount
    text = (
        f"<b>{city}</b>\n\n"
        f"Сумма: {amount}\n\n"
        f"Данные скоро будут доступны."
    )
    await callback.message.edit_text(text, reply_markup=result_keyboard(city, amount))
    await callback.answer("Обновлено до актуальной информации!")
