from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Персонаж", callback_data="menu:profile"),
         InlineKeyboardButton(text="🎒 Инвентарь", callback_data="menu:inventory")],
        [InlineKeyboardButton(text="🗺️ Мир", callback_data="menu:world"),
         InlineKeyboardButton(text="⚔️ Мастерство", callback_data="menu:mastery")],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main")]
    ])
