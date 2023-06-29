from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Определяем кнопки
agree_button = InlineKeyboardButton("Согласен", callback_data="Согласен")
disagree_button = InlineKeyboardButton("Не согласен", callback_data="Не согласен")
numbers_of_feed = [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in [1, 2, 3, 4, 5]]
# Создаем клавиатуру
keyboard = InlineKeyboardMarkup().add(agree_button, disagree_button)
keyboard_buttons = InlineKeyboardMarkup().add(*numbers_of_feed)
