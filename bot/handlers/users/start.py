from aiogram import types
from bot.loader import dp
from .login_register_keyboard import kb
import datetime
from bot.utils.database_connector import cursor, connection_database


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer(f"Привіт, {message.from_user.full_name}!\nУвійдіть або зареєструйтесь", reply_markup=kb)


@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    task_text = message.text.replace("/add", "").strip()

    sql = 'INSERT INTO `task`(`text`, `completed`, `updated_at`) VALUES (%s, %s, %s)'
    val = (task_text, False, datetime.datetime.utcnow())
    cursor.execute(sql, val)
    connection_database.commit()

    await message.reply(f"Task '{task_text}' added!")


@dp.message_handler(commands=['show'])
async def show_tasks(message: types.Message):
    sql = 'SELECT * FROM `task`;'
    cursor.execute(sql)
    tasks = cursor.fetchall()

    tasks_list = "\n".join([f"{task[0]}. {task[1]}" for task in tasks])

    await message.reply(f"Tasks:\n{tasks_list}")
