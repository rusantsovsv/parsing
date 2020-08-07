import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {'accept': '*/*',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

base_url = 'https://habr.com/ru/search/?q=data+science#h'

def parse_habr(base_url=base_url, headers=headers):
    # создадим сессию
    session = requests.Session()

    # эмулируем открытие страниц в браузере
    request = session.get(base_url, headers=headers)


    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        # список имен постов
        posts = soup.find_all('li', attrs={'class': 'content-list__item content-list__item_post shortcuts_item'})

        #print(posts)
        data = {'user_name': [],
                'date': [],
                'title': [],
                'likes': [],
                'tags': []}

        for li in posts:
            # найдем все заголовки на странице и добавим в словарь
            head = li.find('a', {'class': 'post__title_link'}).text
            data['title'].append(head)

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
                data['likes'].append(int(vot.text[1:]))

            # наконец, добавим теги. Их может быть несколько, нужно выделить их из другого блока li
            tags_list = li.find_all('li', attrs={'class': 'inline-list__item inline-list__item_hub'})
            tags_list_for_dict = []
            for tag in tags_list:
                name = tag.find('a', {'class': 'inline-list__item-link hub-link'}).text
                tags_list_for_dict.append(name)
            data['tags'].append(','.join(tags_list_for_dict))

        # собираем словарь в объект pandas и возвращаем его

        return(pd.DataFrame.from_dict(data))


print(parse_habr())

