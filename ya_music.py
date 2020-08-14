import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {'accept': '*/*',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

base_url = 'https://music.yandex.ru/users/serega408ya/playlists/3'


def parse_ya_music(base_url, headers):
    # создадим сессию
    session = requests.Session()
    # эмулируем открытие страниц в браузере
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        # список песен
        songs = soup.find_all('div', attrs={'class': 'd-track__overflowable-wrapper deco-typo-secondary block-layout'})
        data = {'artist': [], 'name_song': []}
        for song in songs:
            # найдем название песни
            name = song.find('div', attrs={'class': 'd-track__name'}).text

            # имя исполнителя
            artist = song.find('div', attrs={'class': 'd-track__meta'}).text

            # добавляем полученные данные к словарю
            data['name_song'].append(name)
            data['artist'].append(artist)
        return pd.DataFrame.from_dict(data)

playlist = parse_ya_music(base_url, headers)

