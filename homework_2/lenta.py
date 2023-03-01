# Урок 2. Парсинг данных. HTML, DOM, XPath
# Написать приложение и функцию, которые собирают основные новости с сайта на выбор dzen.ru, lenta.ru, mail.ru .
# Для парсинга использовать XPath
# Структура данных должна содержать:
# * название источника
# * наименование новости
# * ссылку на новость
# * дата публикации
#
# минимум один сайт максимум все

import requests
from lxml import html
from pprint import pprint

url = 'https://lenta.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

all_news = dom.xpath('//main/div/section/div/div/div/a')

all_news_dict = {}
for news in all_news:
    title = news.xpath('./div/span/text()')[0]
    link = url + news.xpath('./@href')[0]
    time = news.xpath('./div/div/time/text()')
    all_news_dict[title] = {
        'ссылка': link,
        'время публикации': time,
    }

pprint(all_news_dict)
