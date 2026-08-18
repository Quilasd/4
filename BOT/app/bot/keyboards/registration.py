from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def world_menu(worlds: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"world:{world_id}")]
            for world_id, name in worlds
        ]
        + [[InlineKeyboardButton(text="➕ Создать мир", callback_data="world:create")]]
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


def race_menu(races: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=race, callback_data=f"race:{race}")]
            for race in races
        ]
    )
