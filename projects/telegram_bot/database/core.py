import requests
import json
import os
from config_data import config
from urllib.parse import quote

HEADERS = {
    "accept": "application/json",
    "X-API-KEY": config.API_KEY
}

genres = requests.get('https://api.poiskkino.dev/v1/movie/possible-values-by-field?field=genres.name', headers=HEADERS).json()
GENRES = []
for genre in genres:
    GENRES.append(genre['name'])
GENRES.append('0')

URL = 'https://api.kinopoisk.dev/v1.4/movie/'
NOT_NULL = '&notNullFields=name&notNullFields=ageRating&notNullFields=rating.imdb&notNullFields=description&notNullFields=year&notNullFields=poster.url&notNullFields=logo.url'


def search(data: dict) -> list:
    ''' Ищет данные в базе КП в соответствии с алгоритмом. На вход принимает данные, которые ввёл пользватель,
     на выход даёт список из найденных фильмов и сериалов'''
    how = data['how']
    if how == 'name':
        title = quote(data['init'])
    if data['genre'] == '0':
        if how == 'name':
            url = f'{URL}search?page=1&limit={data['variants']}&query={title}{NOT_NULL}'
        elif how == 'rating':
            rate = data['init']
            if rate > 9.5:
                rate = '9-10'
            elif rate < 0.5:
                rate = '0-1'
            else:
                rate = f'{data['init'] - 0.25}-{data['init'] + 0.25}'
            url = f'{URL}random?&rating.imdb={rate}{NOT_NULL}'
        elif how == 'h_budget':
            url = f'{URL}random?&budget.value=100000000-1000000000{NOT_NULL}'
        elif how == 'l_budget':
            url = f'{URL}random?&budget.value=10000-500000{NOT_NULL}'
    else:
        if isinstance(data['genre'], list):
            genre = ''
            for genre_name in data['genre']:
                genre += '&genres.name=%2B' + quote(genre_name)
        else:
            genre = '&genres.name=' + quote(data['genre'])
        if how == 'name':
            url = f'{URL}search?page=1&limit={data['variants']}&query={title}{genre}{NOT_NULL}'
        elif how == 'rating':
            rate = data['init']
            if rate > 9.5:
                rate = '9.5-10'
            elif rate < 0.5:
                rate = '0-0.5'
            else:
                rate = f'{data['init']-0.25}-{data['init']+0.25}'
            url = f'{URL}random?&rating.imdb={rate}{genre}{NOT_NULL}'
        elif how == 'h_budget':
            url = f'{URL}random?&budget.value=100000000-9999999999999999999999999{genre}{NOT_NULL}'
        elif how == 'l_budget':
            url = f'{URL}random?&budget.value=0-10000000{genre}{NOT_NULL}'
    if how == 'name':
        db = requests.get(url, headers=HEADERS)
        db = json.loads(db.text)['docs']
    else:
        db = []
        for _ in range(int(data['variants'])):
            jason = json.loads(requests.get(url, headers=HEADERS).text)
            if jason and jason not in db:
                db.append(jason)
        if how == 'rating' and len(db) < data['variants']:
            if data['genre'] == '0':
                url = f'{URL}random?&rating.kp={rate}{NOT_NULL}'
            else:
                url = f'{URL}random?&rating.imdb={rate}{genre}{NOT_NULL}'
            for _ in range(int(data['variants'])-len(db)):
                jason = json.loads(requests.get(url, headers=HEADERS).text)
                if jason and jason not in db:
                    db.append(jason)
    return db


def poster(data: dict) -> str:
    ''' На вход получает данные о фильме, открывает его постер и даёт на выход расположение этого постера '''
    p = requests.get(data.get('poster').get('url'))
    with open(os.path.join("database", "poster.jpg"), "wb") as out:
        out.write(p.content)
    return os.path.abspath(os.path.join("database", "poster.jpg"))


def show(data: dict) -> str:
    ''' Принимает на вход фильм и даёт на выход текстовую информацию о нём '''
    genre_str = ''
    for genre in data.get('genres', [{}]):
        genre_str += genre.get('name', '') + ', '
    genre_str = genre_str[:-2]
    state_str = ''
    for state in data.get('countries', [{}]):
        state_str += state.get('name', '') + ', '
    state_str = state_str[:-2]
    age = str(data.get('ageRating'))
    if age:
        age += '+'
    text = f'{data.get("name")}, {data.get('year')} год, {state_str}\nЖанры: {genre_str}\nРейтинг на КП: {data.get('rating', {}).get('kp', "отсутствует")}\nРейтинг на IMDB: {data.get('rating', {}).get('imdb', "отсутствует")}\nВозрастной рейтинг: {age}\n\nОписание: {data.get("description")}'
    return text