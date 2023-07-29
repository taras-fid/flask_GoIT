from unittest.mock import AsyncMock
import pytest
from bot.handlers.users import start, login_register_keyboard


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await start.bot_start(message)
    message.answer.assert_called_with(f"Привіт!\nУвійдіть або зареєструйтесь", reply_markup=login_register_keyboard.kb)
