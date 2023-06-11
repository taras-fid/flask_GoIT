from aiogram import types

kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='change age', callback_data='change_age_callback')],
        [types.InlineKeyboardButton(text='change gender', callback_data='change_gender_callback')],
        [types.InlineKeyboardButton(text='change email', callback_data='change_email_callback')],
        [types.InlineKeyboardButton(text='change password', callback_data='change_password_callback')],
    ]
)

kb_gender = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text='male', callback_data='male_gender_change_callback')],
        [types.InlineKeyboardButton(text='female', callback_data='female_gender_change_callback')],
        [types.InlineKeyboardButton(text='other', callback_data='other_gender_change_callback')],
    ]
)