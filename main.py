import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN

# Замените YOUR_TOKEN на токен вашего бота
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
    url = 'https://lenta.ru/parts/news/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    news_titles = soup.find_all('li', class_='parts-page__item')
    last_one_news = news_titles[:1]
    # Отправляем заголовки новостей в чат
    for title in last_one_news:
        title_text = title.find('h3')
        if title_text is not None:
            title_text = title_text.text.strip()
            title_link = title.find('a')['href']
            if not title_link.startswith('http://') and not title_link.startswith('https://'):
                await message.answer(f"{title_text}: 'https://lenta.ru/{title_link}")
            else:
                await message.answer(f"{title_text} : {title_link}")


if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp, skip_updates=True)
