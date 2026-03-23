from aiogram import Router
from aiogram.types import Message

from app.bot.filters.city_input import CityInputFilter
from app.bot.keyboards.result import result_keyboard

router = Router()


@router.message(CityInputFilter())
async def handle_city_query(message: Message, city: str, amount: int) -> None:
    text = (
        f"<b>{city}</b>\n\n"
        f"Сумма: {amount}\n\n"
        f"Данные скоро будут доступны."
    )
    await message.answer(text, reply_markup=result_keyboard(city, amount))
