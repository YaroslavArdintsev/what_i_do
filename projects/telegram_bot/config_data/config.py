import os
import dotenv

if not dotenv.find_dotenv():
    exit('Переменные окружения отсутствуют')
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
DEFAULT_COMMANDS = (
('start', 'Запустить бота'),
('help', 'Вывести справку'),
('movie_search', 'поиск фильма/сериала по названию'),
('movie_by_rating', 'поиск фильма/сериала по рейтингу'),
('low_budget_movie', 'фильм/сериал с низким бюджетом'),
('high_budget_movie', 'фильм/сериал с высоким бюджетом'),
('history', 'история запросов')
)