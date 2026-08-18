from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "🌍 Добро пожаловать в новый мир.\n\n"
        "Игровое ядро уже запускается. Регистрация персонажа будет подключена следующим этапом."
    )
