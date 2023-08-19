from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import re
from bot.utils.database_connector import cursor, connection_database
from werkzeug.security import check_password_hash
from .register import regex_email
from .login_register_keyboard import kb


class LoginStatesGroup(StatesGroup):

    email = State()
    password = State()


@dp.callback_query_handler(text='login_callback')
async def register_callback_function(call: types.CallbackQuery):
    await call.answer('Let check is it you! Enter ur email pls <3')
    await LoginStatesGroup.email.set()


@dp.message_handler(state=LoginStatesGroup.email)
async def username_state_function(message: types.Message, state: FSMContext):
    if re.fullmatch(regex_email, message.text):
        sql = f"SELECT `password_hash` FROM `user` WHERE `email` = '{message.text}';"
        cursor.execute(sql)
        password = cursor.fetchone()
        if password:
            async with state.proxy() as data:
                data['password'] = password[0]
                data['false_password_counter'] = 0
            await message.answer('Now pls enter ur password\nDon`t worry nobody will see it :-)')
            await LoginStatesGroup.next()
        else:
            kb['inline_keyboard'].next().pop()
            await message.answer(f'there is no user with this email, try again or register', reply_markup=kb)
    else:
        await message.answer('email must be like "example@email.com"')


@dp.message_handler(state=LoginStatesGroup.password)
async def password_state_function(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['false_password_counter'] != 3:
            if check_password_hash(data['password'], message.text):
                await message.answer('login passed!')
                await state.reset_state()
                await LoginStatesGroup.email.set()
            else:
                await message.answer('wrong password.')
                data['false_password_counter'] += 1
        else:
            await message.answer('you are blocked... trust this msg pls, GO OUT BASTARD!')
