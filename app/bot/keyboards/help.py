from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.utils.config import BUTTON_TEXT_BACKMENU, CUSTOM_EMOJI_BACKMENU


def help_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BUTTON_TEXT_BACKMENU,
                    callback_data="view_menu",
                    style="primary",
                    icon_custom_emoji_id=CUSTOM_EMOJI_BACKMENU,
                )
            ]
        ]
    )
