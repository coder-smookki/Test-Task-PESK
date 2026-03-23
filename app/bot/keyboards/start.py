from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.config import BUTTON_TEXT_SEARCH, BUTTON_TEXT_HELP, \
    CUSTOM_EMOJI_SEARCH, CUSTOM_EMOJI_HELP


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BUTTON_TEXT_SEARCH,
                callback_data="search",
                style="success",
                icon_custom_emoji_id=CUSTOM_EMOJI_SEARCH
            ),
            InlineKeyboardButton(
                text=BUTTON_TEXT_HELP,
                callback_data="help",
                style="primary",
                icon_custom_emoji_id=CUSTOM_EMOJI_HELP
            ),
        ]
    ])
