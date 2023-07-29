from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class WalletStatesGroup(StatesGroup):

    add = State()
    odd = State()


kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='ADD', callback_data='add_callback')],
        [types.InlineKeyboardButton(text='ODD', callback_data='odd_callback')],
        [types.InlineKeyboardButton(text='BALANCE', callback_data='balance_callback')]
    ]
)


@dp.callback_query_handler(text='add_callback')
async def add_callback_function(call: types.CallbackQuery):
    await call.answer('now enter add amount')
    await WalletStatesGroup.add.set()


@dp.callback_query_handler(text='odd_callback')
async def odd_callback_function(call: types.CallbackQuery):
    await call.answer('now enter odd amount')
    await WalletStatesGroup.odd.set()


@dp.message_handler(lambda message: message.text.lstrip("-").isdigit(), state=WalletStatesGroup.add)
async def add_state_function(message: types.Message, state: FSMContext):
    with open('txt.txt', mode='r') as file:
        balance = file.read()
    with open('txt.txt', mode='w') as file:
        file.write(str(int(balance) + int(message.text)))
    await message.answer(f'ur balance is upped for {message.text}')
    await state.reset_state()


@dp.message_handler(lambda message: message.text.lstrip("-").isdigit(), state=WalletStatesGroup.odd)
async def odd_state_function(message: types.Message, state: FSMContext):
    with open('txt.txt', mode='r') as file:
        balance = file.read()
    with open('txt.txt', mode='w') as file:
        file.write(str(int(balance) - int(message.text)))
    await message.answer(f'ur balance is down for {message.text}')
    await state.reset_state()


@dp.callback_query_handler(text='balance_callback')
async def balance_callback_function(call: types.CallbackQuery):
    with open('txt.txt', mode='r') as file:
        balance = file.read()
        await call.message.answer(f'balance: {balance}')
