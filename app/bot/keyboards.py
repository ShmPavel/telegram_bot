from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Записать сообщение", callback_data="menu:save")],
            [InlineKeyboardButton(text="Выдать записанное", callback_data="menu:list")],
        ]
    )