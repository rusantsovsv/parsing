import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlite3 as sl
from tqdm.auto import trange      # для мониторинга выполнения циклов


# Настроим отображение таблиц в Atom
pd.options.display.html.table_schema = True
pd.options.display.max_rows = None

pd.set_option('display.width', 200)
pd.set_option("display.max_columns", 10)


headers = {'accept': '*/*',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

# разделим url с запросом на 2 части для добавления нужного номера страницы
base_url = ['https://habr.com/ru/search/page', '/?q=data+science&target_type=posts&flow=&order_by=relevance']


def parse_habr(base_url=base_url, headers=headers, num_page='0'):
    # создадим сессию
    session = requests.Session()
    url = base_url[0] + num_page + base_url[1]
    # эмулируем открытие страниц в браузере
    request = session.get(url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        # список имен постов
        posts = soup.find_all('li', attrs={'class': 'content-list__item content-list__item_post shortcuts_item'})

        data = {'user_name': [],
                'date': [],
                'title': [],
                'likes': [],
                'tags': [],
                'post_link': []}

        for li in posts:
            # найдем все заголовки на странице и добавим в словарь

            head = li.find('a', {'class': 'post__title_link'})
            if head is None:
                continue
            else:
                data['title'].append(head.text)

            # сохраним ссылку на пост
            data['post_link'].append(head['href'])
            # найдем всех авторов
            author = li.find('span', {'class': 'user-info__nickname user-info__nickname_small'}).text
            data['user_name'].append(author)

            # найдем даты создания постов
            date = li.find('span', {'class': 'post__time'}).text
            data['date'].append(date)

            # зафиксируем количество лайков. Если лайков нет - пишем 0
            vot = li.find('span', {'class': 'post-stats__result-counter voting-wjt__counter_positive'})
            if vot is None:
                data['likes'].append(0)
            else:
                data['likes'].append(vot.text)

            # наконец, добавим теги. Их может быть несколько, нужно выделить их из другого блока li
            tags_list = li.find_all('li', attrs={'class': 'inline-list__item inline-list__item_hub'})
            tags_list_for_dict = []
            for tag in tags_list:
                name = tag.find('a', {'class': 'inline-list__item-link hub-link'}).text
                tags_list_for_dict.append(name)
            data['tags'].append(','.join(tags_list_for_dict))

    else:
        print(f'Статус запроса {request.status_code}')
        return
    # собираем словарь в объект pandas и возвращаем его

    return pd.DataFrame.from_dict(data)


# создадим итоговый датасет
z = pd.DataFrame.from_dict({' user_name': [],
                            'date': [],
                            'title': [],
                            'likes': [],
                            'tags': [],
                            'post_link': []})

"""Запись данных в базу данных SQLite"""

# создаем коннектор
con = sl.connect('db/parse_habr.db')


for i in (str(x) for x in trange(1000)):
    df = parse_habr(num_page=i)
    print(df.head())
    if df.shape == (0, 6):
        print(f'На странице {i} ничего нет ((')
        break
    df.to_sql('DATA_SCIENCE', con, if_exists='append', index=False)

# база для анализа готова!!

