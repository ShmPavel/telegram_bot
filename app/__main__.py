import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot.handlers import notes, start
from app.bot.middlewares.db import DbSessionMiddleware
from app.config import settings
from app.db.session import engine


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware())

    dp.include_router(start.router)
    dp.include_router(notes.router)

    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())