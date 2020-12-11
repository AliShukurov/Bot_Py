from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
#Для привета
inline_btn_1 = InlineKeyboardButton('Как заполнить расписание', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

#для заполнения расписания
inline_btn_2 = InlineKeyboardButton('Приступить к расписанию', callback_data='button2')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2)