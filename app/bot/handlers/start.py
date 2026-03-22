from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from app.bot.keyboards.start import start_keyboard

router = Router()

START_PHOTO = FSInputFile("assets/start.jpg")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer_photo(
        photo=START_PHOTO,
        caption=(
            "Привет! Я бот, который расскажет о городе.\n\n"
        ),
        reply_markup=start_keyboard(),
    )
