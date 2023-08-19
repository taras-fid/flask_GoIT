from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot.utils.database_connector import cursor, connection_database
from .order_info_keyboard import dynamic_kb
from datetime import datetime, timedelta, time
import os
from bot.data import config


class OrderStatesGroup(StatesGroup):
    post = State()
    date = State()
    time = State()


@dp.message_handler(commands=['order'])
async def order_start(message: types.Message):
    sql = "SELECT `id`, `name` FROM `post`;"
    cursor.execute(sql)
    arr_posts = cursor.fetchall()
    key_value_post_arr = {}
    for i in arr_posts:
        key_value_post_arr[i[0]] = i[1]
    await message.answer('hi, choose massage', reply_markup=dynamic_kb(key_value_post_arr))
    await OrderStatesGroup.post.set()


@dp.callback_query_handler(state=OrderStatesGroup.post)
async def choose_massage(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['post_id'] = int(call.data)
    tomorrow = datetime.now().date() + timedelta(days=1)
    sql = "SELECT `date` FROM `order` WHERE `date` >= %s AND `date` < %s"
    cursor.execute(sql, (tomorrow, tomorrow + timedelta(days=7)))
    result = cursor.fetchall()
    free_time_slots = {}
    for i in result:
        if str(i[0].date()) not in free_time_slots:
            free_time_slots[str(i[0].date())] = [8, 9, 10, 11, 12, 13, 14, 15, 15]
    for i in result:
        if str(i[0].date()) in free_time_slots:
            free_time_slots[str(i[0].date())].remove(i[0].hour)
    async with state.proxy() as data:
        data['free_slots'] = free_time_slots
    await call.message.answer('hi, choose date', reply_markup=dynamic_kb({i: i for i in free_time_slots}))
    await OrderStatesGroup.date.set()


@dp.callback_query_handler(state=OrderStatesGroup.date)
async def choose_date(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        sql = "SELECT `id` FROM `user` WHERE `telegram_id` = %s;"
        cursor.execute(sql, (call.from_user.id,))
        user_id = cursor.fetchone()[0]
        data['user_id'] = user_id
        await call.message.answer('hi, choose date', reply_markup=dynamic_kb({i: i for i in data['free_slots'][call.data]}))
        data['date'] = call.data
        await OrderStatesGroup.time.set()


@dp.callback_query_handler(state=OrderStatesGroup.time)
async def choose_time(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        sql = 'INSERT INTO `order`(`post_id`, `user_id`, `date`) VALUES (%s, %s, %s)'
        val = (data['post_id'], data['user_id'], data['date']+' '+call.data+':00:00')
        cursor.execute(sql, val)
        connection_database.commit()
        order_id = cursor.lastrowid

        await call.message.answer('Well done! Order saved.')

        filename = f'bill_{order_id}'
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)

        with open(file_path, 'w') as file:
            file.write('Order details:\n')
            file.write(f'User ID: {data["user_id"]}\n')
            file.write(f'Post ID: {data["post_id"]}\n')
            file.write(f'Date: {data["date"]} {call.data}:00:00\n')

        await state.reset_state()
