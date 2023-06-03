from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dynamic_kb(text_btn):
    length = len(text_btn)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_btn[i], callback_data=str(i)) for i in range(0, length)]
        ]
    )


def states_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='city', callback_data='city')],
            [InlineKeyboardButton(text='haircut', callback_data='haircut')],
            [InlineKeyboardButton(text='username', callback_data='username')],
            [InlineKeyboardButton(text='phone', callback_data='phone')],
            [InlineKeyboardButton(text='nothing', callback_data='nothing')],
        ]
    )