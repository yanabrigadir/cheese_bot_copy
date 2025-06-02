import logging
import asyncio
import sys

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import settings
from db.database import create_session
from db.dao.user_dao import UserDAO
from services.user_service import UserService

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from tgbot.utils.scheduler import scheduled_job

from tgbot.middlewares.database_middleware import GetSessionMiddleware
from tgbot.middlewares.services_middleware import ServicesMiddleware

from tgbot.handlers.start import router as start_router

bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def start_bot(bot: Bot):
    await bot.send_message(settings.SUPER_ADMIN_ID, 'BOT STARTED')
    logging.info('started')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.SUPER_ADMIN_ID, 'BOT STOPPED')
    logging.info('stopped')


async def create_app() -> web.Application:
    logging.info("Starting in webhook mode...")

    session = await create_session()
    user_dao = UserDAO(session)
    user_service = UserService(user_dao)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scheduled_job,
        IntervalTrigger(minutes=1),
        args=[bot, user_service]
    )
    scheduler.start()

    dp = Dispatcher()
    dp.include_routers(
        start_router
    )

    dp.update.middleware(GetSessionMiddleware())
    dp.update.middleware(ServicesMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    app = web.Application()
    app["bot"] = bot

    SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=settings.WEBHOOK_SECRET).register(
        app, path=settings.get_webhook_path()
    )

    setup_application(app, dp, bot=bot)

    async def on_startup(app):
        await bot.set_webhook(settings.get_webhook_url(), secret_token=settings.WEBHOOK_SECRET)

    async def on_shutdown(app):
        await bot.delete_webhook()
        await bot.session.close()

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    web.run_app(create_app(), host=settings.WEBAPP_HOST, port=settings.WEBAPP_PORT)