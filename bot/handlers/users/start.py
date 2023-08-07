from aiogram import types
from bot.loader import dp
from .login_register_keyboard import kb


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer(f"Привіт, {message.from_user.full_name}!\nУвійдіть або зареєструйтесь", reply_markup=kb)
