from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.config import (
    BUTTON_TEXT_REFRESH,
    BUTTON_TEXT_NEW_SEARCH,
    BUTTON_TEXT_BACKMENU,
    CUSTOM_EMOJI_REFRESH,
    CUSTOM_EMOJI_NEW_SEARCH,
    CUSTOM_EMOJI_BACKMENU,
)


class RefreshCallback(CallbackData, prefix="refresh"):
    city: str
    amount: int


def result_keyboard(city: str, amount: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BUTTON_TEXT_REFRESH,
                callback_data=RefreshCallback(city=city, amount=amount).pack(),
                style="primary",
                icon_custom_emoji_id=CUSTOM_EMOJI_REFRESH,
            ),
            InlineKeyboardButton(
                text=BUTTON_TEXT_NEW_SEARCH,
                callback_data="new_search",
                style="success",
                icon_custom_emoji_id=CUSTOM_EMOJI_NEW_SEARCH,
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTON_TEXT_BACKMENU,
                callback_data="view_menu",
                style="danger",
                icon_custom_emoji_id=CUSTOM_EMOJI_BACKMENU,
            ),
        ],
    ])
