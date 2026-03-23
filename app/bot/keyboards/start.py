from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.utils.config import BUTTON_TEXT_HELP, BUTTON_TEXT_SEARCH, CUSTOM_EMOJI_HELP, CUSTOM_EMOJI_SEARCH


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BUTTON_TEXT_SEARCH,
                    callback_data="search",
                    style="success",
                    icon_custom_emoji_id=CUSTOM_EMOJI_SEARCH,
                ),
                InlineKeyboardButton(
                    text=BUTTON_TEXT_HELP, callback_data="help", style="primary", icon_custom_emoji_id=CUSTOM_EMOJI_HELP
                ),
            ]
        ]
    )
