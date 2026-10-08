import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.bot.handlers import notes, start
from app.bot.middlewares.db import DbSessionMiddleware
from app.config import settings
from app.db.session import engine

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{settings.webhook_base_url}{WEBHOOK_PATH}"
HOST = "0.0.0.0"
PORT = 8080


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    await engine.dispose()
    await bot.session.close()


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware())

    dp.include_router(start.router)
    dp.include_router(notes.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()