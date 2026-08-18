import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.routers.game import router as game_router
from app.bot.routers.registration import router as registration_router
from app.config.settings import get_settings


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level.upper())

    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(registration_router)
    dp.include_router(game_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
