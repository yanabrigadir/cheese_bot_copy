from datetime import datetime, UTC, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot
from aiogram.types import FSInputFile
import logging

from services.user_service import UserService
from tgbot.keyboards.inline_kb import payments_methods_kb


async def scheduled_job(bot: Bot, user_service: UserService):
    users = await user_service.get_all_users()
    for user in users:
        last_message = user.last_message.replace(tzinfo=ZoneInfo("UTC"))
        difference = datetime.now(UTC) - last_message

        try:
            if difference > timedelta(minutes=3):
                text = 'Кстати, у нас в канале есть пост, под которым участники Чиза скинули <b>19.000 своих самых лучших фото</b> из бота 👉<a href="https://t.me/cheeseaiapp/147">пост</a>'
                await bot.send_photo(
                    chat_id=user.id,
                    caption=text,
                    photo=FSInputFile('tgbot/media/by_the_way.jpg')
                )
            elif difference > timedelta(minutes=2):
                text = ('Кстати, обязательно подпишись на наш канал @cheeseaiapp.\n\n'
                        'Внутри публикуем оригинальные идеи стилей для ваших фото, а также актуальные новости.')
                await bot.send_message(user.id, text)
            elif difference > timedelta(minutes=1):
                text = ('Ладно, вот в 4 раза дешевле.\n\n'
                        '<b>329Р</b> за пробный период!\n\n'
                        'И за это ты получаешь\n'
                        '✔️ 10 фотографий\n'
                        '✔️ 100 стилей на выбор\n'
                        '✔️ 1 модель аватара\n'
                        '✔️ Канал с 5.000 идей фото\n\n'
                        'Попробуй на 10 фотках, потом решишь нужно ли тебе еще 👍')
                await bot.send_photo(
                    chat_id=user.id,
                    caption=text,
                    photo=FSInputFile('tgbot/media/attempt_1.jpg'),
                    reply_markup=payments_methods_kb()
                )
            else:
                continue
        except Exception as e:
            logging.error(f"Failed to send message {user.id}: {e}")
