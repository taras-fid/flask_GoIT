from aiogram import executor
import bot.loader
import bot.handlers
from bot.utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

executor.start_polling(loader.dp, on_startup=on_startup, skip_updates=True)
