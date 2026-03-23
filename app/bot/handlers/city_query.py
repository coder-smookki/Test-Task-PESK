import asyncio

from aiogram import Router
from aiogram.types import Message

from app.bot.filters.city_input import CityInputFilter
from app.bot.keyboards.result import result_keyboard
from app.bot.utils.config import LOADING_FRAMES, LOADING_DELAY, ERROR_CITY_NOT_FOUND
from app.bot.utils.formatters import format_result
from app.bot.utils.photo_cache import get_photo, save_photo_id
from app.services.city_info import get_city_info

router = Router()


async def _animate_loading(wait: Message, stop: asyncio.Event) -> None:
    idx = 0
    while not stop.is_set():
        frame = LOADING_FRAMES[idx % len(LOADING_FRAMES)]
        try:
            await wait.edit_text(frame)
        except Exception:
            pass
        idx += 1
        try:
            await asyncio.wait_for(stop.wait(), timeout=LOADING_DELAY)
            return
        except asyncio.TimeoutError:
            pass


@router.message(CityInputFilter())
async def handle_city_query(message: Message, city: str, amount: int) -> None:
    wait = await message.answer(LOADING_FRAMES[0])

    stop = asyncio.Event()
    anim_task = asyncio.create_task(_animate_loading(wait, stop))

    try:
        data = await get_city_info(city, amount)
    finally:
        stop.set()
        await anim_task

    await wait.delete()

    if data is None:
        await message.answer(ERROR_CITY_NOT_FOUND)
        return

    result = await message.answer_photo(
        photo=get_photo("result"),
        caption=format_result(data),
        reply_markup=result_keyboard(city, amount),
    )
    save_photo_id("result", result)
