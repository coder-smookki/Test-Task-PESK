from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Поиск",
                callback_data="search",
                style="success",
                icon_custom_emoji_id="5348544647977254780"
            ),
            InlineKeyboardButton(
                text="Помощь",
                callback_data="help",
                style="primary",
                icon_custom_emoji_id="5348337458754894202"
            ),
        ]
    ])
