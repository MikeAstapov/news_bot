import feedparser

class NewsParser:
    def __init__(self, rss_url, num_news):
        self.rss_url = rss_url
        self.num_news = num_news

    def get_news(self):
        feed = feedparser.parse(self.rss_url)

        news_list = []
        count = 0
        for entry in feed.entries:
            if count >= self.num_news:
                break
            enclosures = entry.get('enclosures', [])
            for enclosure in enclosures:
                if enclosure.get('type', '').startswith('image'):
                    news_list.append({
                        'text': entry.get('title', '') + ": " + entry.get('summary', ''),
                        'photo': enclosure.get('href', '')
                    })
                    count += 1

        return news_list



