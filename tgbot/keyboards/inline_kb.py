from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

def start_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Далее',
            callback_data='next'
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Оплатить',
            callback_data='pay'
        )
    )

    return builder.as_markup()


def explanation_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Понятно, дальше',
            callback_data='thank_you_next'
        )
    )

    return builder.as_markup()


def how_much_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='А сколько стоит?',
            callback_data='how_much'
        )
    )

    return builder.as_markup()


def payments_methods_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Карта в РФ',
            callback_data='payment'
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Stripe (в $)',
            callback_data='payment'
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Lava (в $)',
            callback_data='payment'
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='Служба заботы',
            url='t.me/yanabrigadir'
        )
    )

    builder.adjust(2)

    return builder.as_markup()

