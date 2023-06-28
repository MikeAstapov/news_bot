import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram.utils import executor

import db
from config import TOKEN
from buttons import keyboard
from db import add_new_user

# Замените token на токен вашего бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
date = datetime.now().date()
agreement = False
db.sql_start()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    # отправляем приветственное сообщение
    await message.answer(
        "Привет! Я новостной бот. буду держать тебя в курсе последних событий.Введи /news чтобы увидеть"
        " последние новости")
    await message.answer("Нажми кнопку согласен, если хочешь получать новости в режиме онлайн", reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data == 'Согласен')
async def agree_keyboard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    params = (callback_query.from_user.id, callback_query.from_user.full_name, date, agreement == True)
    add_new_user(params)
    await callback_query.message.answer("Вы согласились получать новости онлайн.Для отмены используйте меню /start")


@dp.callback_query_handler(lambda query: query.data == 'Не согласен')
async def agree_keyboard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    params = (callback_query.from_user.id, callback_query.from_user.full_name, date, agreement==False)
    add_new_user(params)
    await callback_query.message.answer(
        "Вы не согласились получать новости онлайн.Используйте меню /start если передумаете :)")


# Обработчик команды /news
@dp.message_handler(commands=['news'])
async def send_news(message: types.Message):
    pass

    # Отправляем заголовки новостей в чат


if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp, skip_updates=True)
