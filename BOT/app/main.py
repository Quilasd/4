import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot.routers.start import router as start_router
from app.config.settings import get_settings


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level.upper())

    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(start_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
