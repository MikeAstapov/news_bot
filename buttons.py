from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Определяем кнопки
agree_button = InlineKeyboardButton("Согласен", callback_data="Согласен")
disagree_button = InlineKeyboardButton("Не согласен", callback_data="Не согласен")

# Создаем клавиатуру
keyboard = InlineKeyboardMarkup().add(agree_button, disagree_button)