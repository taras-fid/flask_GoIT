from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from bot.utils.database_connector import cursor, connection_database
from .user_info_kb import kb, kb_gender


class ChangeInfoStates(StatesGroup):
    ageState = State()
    genderState = State()


@dp.message_handler(commands='user_info')
async def get_user_info(message: types.Message, state: FSMContext):
    sql = f"SELECT `age`, `gender`, `email`, `password_hash` FROM `user` WHERE `telegram_id` = '{message.from_user.id}';"
    cursor.execute(sql)
    async with state.proxy() as data:
        data_from_db = cursor.fetchone()
        data['age'] = data_from_db[0]
        data['gender'] = data_from_db[1]
        data['email'] = data_from_db[2]
        data['password_hash'] = data_from_db[3]
        await message.answer(f"ur info:\nage: {data['age']}\ngender: {data['gender']}\nemail: {data['email']}",
                             reply_markup=kb)


@dp.callback_query_handler(text='change_age_callback')
async def change_age_callback_function(call: types.CallbackQuery, state: FSMContext):
    await call.answer('now enter ur age')
    await ChangeInfoStates.ageState.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=ChangeInfoStates.ageState)
async def age_state_function(message: types.Message, state: FSMContext):
    sql = f"UPDATE `user` SET `age`={message.text} WHERE `telegram_id`={str(message.from_user.id)};"
    cursor.execute(sql)
    connection_database.commit()
    await state.reset_state()
    await message.answer('your age was changed!')


@dp.callback_query_handler(text='change_gender_callback')
async def change_gender_callback_function(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(text='now choose ur gender', chat_id=call.from_user.id, reply_markup=kb_gender)
    await ChangeInfoStates.genderState.set()


@dp.callback_query_handler(state=ChangeInfoStates.genderState)
async def gender_state_function(call: types.CallbackQuery, state: FSMContext):
    sql = f"UPDATE `user` SET `gender`='{call.data.replace('_gender_change_callback', '')}' WHERE `telegram_id`={str(call.from_user.id)};"
    cursor.execute(sql)
    connection_database.commit()
    await state.reset_state()
    await bot.send_message(text='your gender was changed!', chat_id=call.from_user.id)
