import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import db
from config import TOKEN
from buttons import keyboard, keyboard_buttons
from lenta_news_class import NewsParser
import aioschedule

# Замените token на токен вашего бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
date = datetime.now().date()
db.sql_start()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    params = (message.from_user.id, message.from_user.full_name, date, 0)
    db.add_new_user(params)
    # отправляем приветственное сообщение
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я новостной бот. буду держать тебя в курсе последних событий.Введи /news чтобы увидеть"
        " последние новости")
    await message.answer("Нажми кнопку согласен, если хочешь получать новости в режиме онлайн", reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data == 'Согласен')
async def agree_keyboard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    params = (1, callback_query.from_user.id)
    db.add_user_agreement(params)
    await callback_query.message.answer("Вы согласились получать новости онлайн.Для отмены используйте меню /start")


@dp.callback_query_handler(lambda query: query.data == 'Не согласен')
async def agree_keyboard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    params = (0, callback_query.from_user.id)
    db.delete_user_agreement(params)
    await callback_query.message.answer(
        "Вы не согласились получать новости онлайн.Используйте меню /start если передумаете :)")
    await callback_query.message.answer("С помощью команды /news можете посмотреть последние новости")


# Обработчик команды /news
@dp.message_handler(commands=['news'])
async def send_news(message: types.Message):
    await message.answer("Какое кол-во последних новостей вы хотите увидеть?", reply_markup=keyboard_buttons)


@dp.callback_query_handler(lambda query: query.data in ['1', '2', '3', '4', '5'])
async def return_news_number(callback_query: types.CallbackQuery):
    lenta = NewsParser("https://lenta.ru/rss/top7", int(callback_query.data))
    news_list = lenta.get_news()
    for news in news_list:
        text = news['text']
        photo = news['photo']
        await bot.send_message(callback_query.message.chat.id,
                               f"{text} {photo}")
    await bot.answer_callback_query(callback_query.id)


last_news = None


@dp.message_handler(commands=['spam'])
async def send_message_with_last_news(message):
    global last_news
    lenta = NewsParser("https://lenta.ru/rss/top7", 1)  # Получить только одну новость
    news_list = lenta.get_news()

    if len(news_list) > 0:
        current_news = news_list[0]['text']
        current_foto = news_list[0]['photo']


        if last_news != current_news:
            for user in db.select_all_users_with_agreement():
                await bot.send_message(user[0], current_news + ' ' + current_foto)
        last_news = current_news


@dp.message_handler()
async def command_not_found(message: types.Message):
    await message.delete()
    await message.answer(f"Команда {message.text} не найдена")


async def scheduler():
    aioschedule.every(60).seconds.do(send_message_with_last_news, 'message')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    print("Бот запущен")
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    print(db.select_all_users_with_agreement())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
