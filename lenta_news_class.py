import requests
from bs4 import BeautifulSoup
from typing import List


class LentaNews:
    def __init__(self, num_news: int = 1):
        # Проверяем наличие интернет-соединения
        if not self.check_internet_connection():
            print("Отсутствует интернет-соединение")
            return
        self.url = 'https://lenta.ru/parts/news/'
        self.response = None
        try:
            self.response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return
        self.soup = None
        try:
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except Exception as e:
            print(f"Error: {e}")
            return
        self.news_titles = self.soup.find_all('li', class_='parts-page__item')
        self.last_news = self.news_titles[:num_news]

    def get_news(self) -> List[str]:
        # Создаем пустой список для хранения новостей
        news_list = []

        # Проверяем, есть ли новости
        if not self.last_news:
            # Если нет новостей, добавляем сообщение в список
            news_list.append("Новостей нет. Скорее всего у сайта lenta.ru проблемы :)")
        else:
            # Если есть новости, обрабатываем каждую новость
            for title in self.last_news:
                title_text = title.find('h3')
                if title_text is not None:
                    title_text = title_text.text.strip()
                    title_link = title.find('a')['href']
                    if not title_link.startswith('http://') and not title_link.startswith('https://'):
                        news_list.append(f"{title_text}\n"
                                         f"Текст статьи смотрите по ссылке: https://lenta.ru/{title_link}\n")
                    else:
                        news_list.append(f"{title_text}\n"
                                         f"Текст статьи смотрите по ссылке: {title_link}\n")

        # Возвращаем список новостей
        return news_list

    def check_internet_connection(self) -> bool:
        try:
            requests.get('https://www.google.com/')
            return True
        except requests.exceptions.RequestException:
            return False



