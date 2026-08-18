from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.session import SessionFactory
from app.services.user_service import get_or_create_user

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    if message.from_user is None:
        return

    async with SessionFactory() as session:
        user, created = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
        )

    if created:
        text = (
            "🌍 Добро пожаловать в новый мир!\n\n"
            "Ты зарегистрирован. Следующим шагом выбери мир и создай персонажа."
        )
    else:
        text = "🌍 С возвращением! Твой профиль найден."

    await message.answer(text)
