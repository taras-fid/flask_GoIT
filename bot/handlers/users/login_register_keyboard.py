from aiogram import types

kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='login', callback_data='login_callback')],
        [types.InlineKeyboardButton(text='register', callback_data='register_callback')]
    ]
)