from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot.utils.database_connector import cursor, connection_database
from .user_info_keyboard import dynamic_kb, states_kb


json_db = {
    'City': {
        'Kyiv': {'address': 'St. Kyiv'},
        'Zhytomyr': {'address': 'St. Zhytomyr'},
        'Odessa': {'address': 'St. Odessa'},
    },
    'Haircut': {
        'naliso': 300,
        'pod zero': 299,
        'pod six': 298,
        'crop': 199,
    }
}


class UserInfoStatesGroup(StatesGroup):
    city = State()
    haircut = State()
    username = State()
    phone = State()
    endState = State()


text_btn = [
    ['Kyiv', 'Zhytomyr', 'Odessa'],
    ['naliso', 'pod zero', 'pod six', 'crop'],
    ['Yes', 'No'],
]


@dp.message_handler(commands=['haircut'])
async def haircut_start(message: types.Message):
    await message.answer('hi, choose ur city.', reply_markup=dynamic_kb(text_btn[0]))
    await UserInfoStatesGroup.city.set()


@dp.callback_query_handler(text='0', state=UserInfoStatesGroup.city)
async def choose_first_city(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = text_btn[0][int(call.data)]
    await call.message.answer(f"ви можете знйти нас в місті {text_btn[0][int(call.data)]} за цією адресою: {json_db['City'][text_btn[0][int(call.data)]]['address']}")
    await call.message.answer(f"choose haircut", reply_markup=dynamic_kb(text_btn[1]))
    await UserInfoStatesGroup.haircut.set()


@dp.callback_query_handler(text='1', state=UserInfoStatesGroup.city)
async def choose_second_city(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = text_btn[0][int(call.data)]
    await call.message.answer(f"ви можете знйти нас в місті {text_btn[0][int(call.data)]} за цією адресою: {json_db['City'][text_btn[0][int(call.data)]]['address']}")
    await call.message.answer(f"choose haircut", reply_markup=dynamic_kb(text_btn[1]))
    await UserInfoStatesGroup.haircut.set()


@dp.callback_query_handler(text='2', state=UserInfoStatesGroup.city)
async def choose_third_city(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = text_btn[0][int(call.data)]
    await call.message.answer(f"ви можете знйти нас в місті {text_btn[0][int(call.data)]} за цією адресою: {json_db['City'][text_btn[0][int(call.data)]]['address']}")
    await call.message.answer(f"choose haircut", reply_markup=dynamic_kb(text_btn[1]))
    await UserInfoStatesGroup.haircut.set()


@dp.callback_query_handler(text='0', state=UserInfoStatesGroup.haircut)
async def choose_first_haircut(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['haircut'] = text_btn[1][int(call.data)]
    await call.message.answer(f"обрана зачіска `{text_btn[1][int(call.data)]}` буде коштувати: {json_db['Haircut'][text_btn[1][int(call.data)]]}")
    await call.message.answer(f"enter ur name")
    await UserInfoStatesGroup.username.set()


@dp.callback_query_handler(text='1', state=UserInfoStatesGroup.haircut)
async def choose_second_haircut(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['haircut'] = text_btn[1][int(call.data)]
    await call.message.answer(f"обрана зачіска `{text_btn[1][int(call.data)]}` буде коштувати: {json_db['Haircut'][text_btn[1][int(call.data)]]}")
    await call.message.answer(f"enter ur name")
    await UserInfoStatesGroup.username.set()


@dp.callback_query_handler(text='2', state=UserInfoStatesGroup.haircut)
async def choose_third_haircut(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['haircut'] = text_btn[1][int(call.data)]
    await call.message.answer(f"обрана зачіска `{text_btn[1][int(call.data)]}` буде коштувати: {json_db['Haircut'][text_btn[1][int(call.data)]]}")
    await call.message.answer(f"enter ur name")
    await UserInfoStatesGroup.username.set()


@dp.callback_query_handler(text='3', state=UserInfoStatesGroup.haircut)
async def choose_fourth_haircut(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['haircut'] = text_btn[1][int(call.data)]
    await call.message.answer(f"обрана зачіска `{text_btn[1][int(call.data)]}` буде коштувати: {json_db['Haircut'][text_btn[1][int(call.data)]]}")
    await call.message.answer(f"enter ur name")
    await UserInfoStatesGroup.username.set()


@dp.message_handler(state=UserInfoStatesGroup.username)
async def enter_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text.capitalize()
    await message.answer(f'okey, {message.text.capitalize()}, now enter ur phone, for communication')
    await UserInfoStatesGroup.phone.set()


@dp.message_handler(state=UserInfoStatesGroup.phone)
async def enter_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        await message.answer(f'ty, please confirm the deal'+f'\n{data}', reply_markup=dynamic_kb(text_btn[2]))
    await UserInfoStatesGroup.endState.set()


@dp.callback_query_handler(text='0', state=UserInfoStatesGroup.endState)
async def choose_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Дякуємо, що обрали саме нас, чекаємо на вас.")
    await state.reset_state()


@dp.callback_query_handler(text='1', state=UserInfoStatesGroup.endState)
async def choose_no(call: types.CallbackQuery):
    await call.message.answer(f"Do u want rechoose something.", reply_markup=states_kb())


@dp.callback_query_handler(text='city', state=UserInfoStatesGroup.endState)
async def choose_city_change(call: types.CallbackQuery):
    await call.message.answer('ok, rechoose ur city.', reply_markup=dynamic_kb(text_btn[0]))
    await UserInfoStatesGroup.city.set()


@dp.callback_query_handler(text='haircut', state=UserInfoStatesGroup.endState)
async def choose_city_change(call: types.CallbackQuery):
    await call.message.answer('ok, rechoose ur haircut.', reply_markup=dynamic_kb(text_btn[1]))
    await UserInfoStatesGroup.haircut.set()


@dp.callback_query_handler(text='username', state=UserInfoStatesGroup.endState)
async def choose_city_change(call: types.CallbackQuery):
    await call.message.answer('ok, rewrute ur name.')
    await UserInfoStatesGroup.username.set()


@dp.callback_query_handler(text='phone', state=UserInfoStatesGroup.endState)
async def choose_city_change(call: types.CallbackQuery):
    await call.message.answer('ok, rewrute ur phone.')
    await UserInfoStatesGroup.phone.set()


@dp.callback_query_handler(text='nothing', state=UserInfoStatesGroup.endState)
async def choose_city_change(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('ok')
    await state.reset_state()
