from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def dynamic_kb(text_btn):
    length = len(text_btn)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_btn[i], callback_data=str(i)) for i in text_btn]
        ]
    )