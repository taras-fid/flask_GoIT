from aiogram import types
from bot.loader import dp


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await message.answer("\nСписок команд: \n/start - Почати діалог\n/help - Отримати поміч")
