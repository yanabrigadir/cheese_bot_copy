from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery

from db.dao.user_dao import UserAlreadyExistsError
from services.user_service import UserService

from tgbot.keyboards.inline_kb import (
    start_kb,
    explanation_kb,
    how_much_kb,
    payments_methods_kb
)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, user_service: UserService) -> None:
    tg_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        await user_service.create_user(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
    except UserAlreadyExistsError:
        await user_service.change_user_last_msg(tg_id)

    text = ('Привет! Давай знакомиться 😊\n'
            'Мы — Вова, Артур и Олег, создатели Чиз.\n\n'
            '🧀 ЧИЗ ИИ — <b>это нейросеть,</b> которая создаёт крутые фото с вашим лицом, отражает лучшие черты и раскрывает творческий потенциал!\n\n'
            '💡 Раз уж вы здесь по рекомендации, расскажем, как это работает!')

    await message.answer_photo(
        photo=FSInputFile('tgbot/media/start_photo.jpg'),
        caption=text,
        reply_markup=start_kb()
    )


@router.callback_query(F.data == 'next')
async def examples_query(callback_query: CallbackQuery, user_service: UserService) -> None:
    tg_id = callback_query.from_user.id
    await user_service.change_user_last_msg(tg_id)

    text = ('🔥 Вот примеры того, что каждый день делает ЧИЗ ИИ!\n\n'
            'Это работы обычных пользователей из чата.\n\n'
            '📸 Просто загружаешь несколько своих фото из фотопленки, ИИ обучается твоему аватару и затем рождаются фантастические образы с тобой!')

    await callback_query.message.answer_photo(
        photo=FSInputFile('tgbot/media/examples.jpg'),
        caption=text,
        reply_markup=explanation_kb()
    )
    await callback_query.answer()


@router.callback_query(F.data == 'thank_you_next')
async def final_msg_query(callback_query: CallbackQuery, user_service: UserService) -> None:
    tg_id = callback_query.from_user.id
    await user_service.change_user_last_msg(tg_id)

    text = ('🌟 Уже <b>более 1 000 000 человек</b> попробовали ЧИЗ ИИ! Теперь ваша очередь!\n\n'
            '🎭🧞‍♂️ Два режима на выбор:\n'
            '1️⃣ <b>Готовые идеи</b> — 100+ стилей: от богемных образов до рок-звезды\n'
            '2️⃣ <b>Режим Бога</b> — просто опишите желаемый образ или скидываешь фото референс, а ИИ создаст уникальную фотографию!\n\n'
            '✨ Теперь к волшебству. Так как вы пришли по рекомендации, для вас специальные условия!')

    await callback_query.message.answer_photo(
        photo=FSInputFile('tgbot/media/more_than_million.jpg'),
        caption=text,
        reply_markup=how_much_kb()
    )
    await callback_query.answer()


@router.callback_query(F.data.in_({'how_much', 'pay'}))
async def pay_msg_query(callback_query: CallbackQuery, user_service: UserService) -> None:
    tg_id = callback_query.from_user.id
    await user_service.change_user_last_msg(tg_id)

    text = ('💥 <b>Скидка 73%!</b>\n\n'
            '💰 <b>1390₽</b> вместо <s>5150₽</s>\n\n'
            '📦 В пакет входит\n'
            '✅ 90 фотографий\n'
            '✅ 100 стилей на выбор\n'
            '✅ 1 модель аватара\n'
            '✅ Режим Бога\n'
            '✅ Канал с 5.000 идей\n'
            '💬 Чат с участниками\n\n'
            '⏳ Бонус! При оплате в течение 30 минут — дополнительно 10 генераций в подарок! 🎁')

    await callback_query.message.answer_photo(
        photo=FSInputFile('tgbot/media/pay_msg.jpg'),
        caption=text,
        reply_markup=payments_methods_kb()
    )
    await callback_query.answer()


@router.callback_query(F.data == 'payment')
async def payment_query(callback_query: CallbackQuery, user_service: UserService) -> None:
    tg_id = callback_query.from_user.id
    await user_service.change_user_last_msg(tg_id)

    await callback_query.message.answer('Вы успешно оплатили!')
    await callback_query.answer()
