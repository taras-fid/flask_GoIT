from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import re
from bot.utils.database_connector import cursor, connection_database
from werkzeug.security import generate_password_hash, check_password_hash

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regex_password = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')


class RegisterStatesGroup(StatesGroup):

    username = State()
    email = State()
    password = State()
    repeat_password = State()


@dp.callback_query_handler(text='register_callback')
async def register_callback_function(call: types.CallbackQuery):
    await call.answer('Let start our journey! Enter ur username pls <3')
    await RegisterStatesGroup.username.set()


@dp.message_handler(state=RegisterStatesGroup.username)
async def username_state_function(message: types.Message, state: FSMContext):
    if len(message.text) <= 20:
        async with state.proxy() as data:
            data['username'] = message.text
        await message.answer(f'nice! {message.text.capitalize()} now pls enter ur email')
        await RegisterStatesGroup.next()
    else:
        await message.answer('username must be less than 20 symbols.')


@dp.message_handler(state=RegisterStatesGroup.email)
async def email_state_function(message: types.Message, state: FSMContext):
    if re.fullmatch(regex_email, message.text):
        async with state.proxy() as data:
            data['email'] = message.text
        await message.answer('email saved successfully! Now pls enter ur password\nDon`t worry nobody will see it :-)')
        await RegisterStatesGroup.next()
    else:
        await message.answer('email must be like "example@email.com"')


@dp.message_handler(state=RegisterStatesGroup.password)
async def password_state_function(message: types.Message, state: FSMContext):
    if re.fullmatch(regex_password, message.text):
        async with state.proxy() as data:
            data['password'] = message.text
        await message.answer('password saved successfully! Now pls enter ur password again')
        await RegisterStatesGroup.next()
    else:
        await message.answer('password must contain at least one number, upper and lower case letter and special symbol')


@dp.message_handler(state=RegisterStatesGroup.repeat_password)
async def repeat_password_state_function(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == data['password']:
            sql = 'INSERT INTO `user`(`username`, `email`, `password_hash`, `telegram_id`) VALUES (%s, %s, %s, %s)'
            val = (data['username'], data['email'], generate_password_hash(data['password']), message.from_user.id)
            cursor.execute(sql, val)
            connection_database.commit()
            await message.answer('Well done! Registration passed successfully.')
            await state.reset_state()
            msg = await message.answer(text="/user_info")
            await msg.delete()
        else:
            await message.answer('password must be the same')
