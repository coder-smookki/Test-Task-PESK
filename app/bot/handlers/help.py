from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router = Router()

HELP_PHOTO = FSInputFile("assets/help.jpg")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer_photo(
        photo=HELP_PHOTO,
        caption=(
            "Как пользоваться ботом:"
        ),
        # reply_markup=help_keyboard()
    )