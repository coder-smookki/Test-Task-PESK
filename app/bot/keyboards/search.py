from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.utils.config import BUTTON_TEXT_CANCEL, CUSTOM_EMOJI_CANCEL


def search_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BUTTON_TEXT_CANCEL,
                    callback_data="cancel",
                    style="danger",
                    icon_custom_emoji_id=CUSTOM_EMOJI_CANCEL,
                )
            ]
        ]
    )
