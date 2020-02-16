import requests
from bs4 import BeautifulSoup as bs

# для того, чтобы hh не блокировал меня как бота необходимо в каждом запросе передавать accept
# и user agent

headers = {'accept': '*/*',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

base_url = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&search_period=7&text=python&page=0'
"""
В URL:
area=2 - код города Санкт-Петербург
search_period=7 - период поиска (7 дней)
text=python - текст поиска (например, Python)
page=0 - 1 страница
"""


def hh_parse(base_url, headers):
    jobs = []           # в этот список будем складывать результаты парсинга

    # создадим сессию, чтоб hh думал, что заходит один и тотже пользователь и просматривает вакансии
    session = requests.Session()
    # эмулируем открытие страниц в браузере
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        # получим из необходимых блоков нужную информацию
        for div in divs:
            title = div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text          # получим названия вакансий
            href = div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']        # получим ссылку на вакансию
            company = div.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text     # получим название компании
            # парсим текст вакансии
            text1 = div.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = text1 + ' ' + text2
            jobs.append({'title': title,
                         'href': href,
                         'company': company,
                         'content': content})
        print(len(jobs))        # получили 16 вакансий в словаре!
    else:
        print('ERROR')

hh_parse(base_url, headers)
