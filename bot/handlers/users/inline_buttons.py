from aiogram import types
from loader import dp

kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='login', url='google.com')],
        [types.InlineKeyboardButton(text='register', callback_data='register_callback', request_contact=True)]
    ]
)


@dp.callback_query_handler(text='register_callback')
async def register_callback_function(call: types.CallbackQuery):
    await call.message.answer('register_callback_function')
