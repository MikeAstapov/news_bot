from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN
import lenta_news_class
# Замените token на токен вашего бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    # отправляем приветственное сообщение
    await message.answer(
        "Привет! Я новостной бот. буду держать тебя в курсе последних событий.Введи /news чтобы увидеть"
        "последние новости")


# Обработчик команды /news

@dp.message_handler(commands=['news'])
async def send_news(message: types.Message):
    pass

    # Отправляем заголовки новостей в чат


if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp, skip_updates=True)
