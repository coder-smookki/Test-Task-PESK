from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router = Router()

SEARCH_PHOTO = FSInputFile("assets/search.jpg")


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    await message.answer_photo(
        photo=SEARCH_PHOTO,
        caption=(
            "Сейчас будем искать."
        ),
        # reply_markup=cancel_keyboard()
    )
