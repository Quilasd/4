from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def world_menu(worlds: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"world:{world_id}")]
            for world_id, name in worlds
        ]
        + [[InlineKeyboardButton(text="➕ Создать мир", callback_data="world:create")]]
    )


def continent_menu(continents: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"continent:{key}")]
            for key, name in continents
        ]
    )


def gender_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="♂ Мужской", callback_data="gender:male"),
                InlineKeyboardButton(text="♀ Женский", callback_data="gender:female"),
            ]
        ]
    )


def race_menu(races: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"race:{key}")]
            for key, name in races
        ]
    )
