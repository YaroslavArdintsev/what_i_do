from loader import bot
from telebot.types import Message
from database import core
from keyboards.inline import usual_inline, historic_inline
from database.history import User, Request
import math
from telebot.handler_backends import State, StatesGroup
from datetime import date

class Search(StatesGroup):
    '''
    Группа состояниц пользователя в диалоге. Включает в себя:

    1) "хаб", в котором ничего не проиходит
    2) получение изначальных данных (названия/рейтинга) фильма
    3) получение жанра фильма
    4) получения кол-ва вариантов в выдаче
    '''
    hub = State()
    name = State()
    genre = State()
    variants = State()


@bot.message_handler(commands=['start'])
def lets_get_it_started(message: Message) -> None:
    ''' Реагирует на /start, представляется. Вводит пользователя в состояние "хаба" и ждёт новых команд. '''

    bot.send_message(message.from_user.id, 'Гм... З-здравствуйте. Я — Цумуги Широгане. Я ваша скромная помощница в поисках... кхм... фильмов и сериалов. Моя тайная мастерская уже полна идеями и каталогами.\nА, и ещё... пожалуйста, нажмите /help, если хотите узнать, какие у меня есть... инструменты для творческого поиска. Буду рада помочь!')
    bot.set_state(message.from_user.id, Search.hub, message.chat.id)


@bot.message_handler(commands=['help'])
def show_me_what_youve_got(message: Message) -> None:
    ''' Реагирует на /help, рассказывает о других командах.
    Вводит пользователя в состояние "хаба" и ждёт новых команд. '''

    bot.send_message(message.from_user.id,
                     'Ох... Значит, так... Вот то, с помощью чего я ищу кино. М-мои команды...\n/movie_search — поиск по названию... словно отыскиваешь потерянную цитату в огромной библиотеке\n/movie_by_rating — если вам важна оценка других зрителей... в смысле рейтинг\n/low_budget_movie — поиск скромных, но, быть может, очень душевных работ, где бюджет — не главный герой\n/high_budget_movie — а здесь, наоборот, пышные постановки, где каждый кадр стоит целое состояние\n/history — это... словно заглянуть в черновики и эскизы, чтобы увидеть, что мы искали раньше')
    bot.set_state(message.from_user.id, Search.hub, message.chat.id)


@bot.message_handler(commands=['history'])
def go_down_in_history(message: Message) -> None:
    ''' Реагирует на /history, собирает историю запросов пользователя и передаёт её
    вместе с ID пользователя в ф-ю show модуля keyboards.inline.historic_inline
    для последующей отправки истории запросов пользователю '''

    user = User.get_or_none(User.user_id == message.from_user.id)
    if user is None:
        bot.reply_to(message, 'Простите, но... Похоже, вы пока ещё ничего не искали. Исправите это?')
        return
    requests = user.requests.order_by(-Request.request_id, -Request.date).limit(10)
    result = list(requests)
    historic_inline.show(message.from_user.id, result)


@bot.message_handler(commands=['movie_search'])
def search_name(message: Message) -> None:
    ''' Реагирует на /movie_search, спрашивает название фильма/сериала.
    Вводит пользователя в состояние получения начальных данных. '''

    bot.set_state(message.from_user.id, Search.name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how'] = 'name'
    bot.send_message(message.from_user.id,
                     f'Х-хорошо, {message.from_user.username}, я всё поняла...\nТеперь, пожалуйста, назовите имя фильма или сериала, который вы хотите, чтобы я отыскала!')


@bot.message_handler(commands=['movie_by_rating'])
def search_rating(message: Message) -> None:
    ''' Реагирует на /movie_by_rating, спрашивает рейтинг фильма/сериала.
        Вводит пользователя в состояние получения начальных данных. '''

    bot.set_state(message.from_user.id, Search.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Х-хорошо, {message.from_user.username}, я всё поняла...\nТогда назовите рейтинг сокровища, которое хотите найти!')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how'] = 'rating'


@bot.message_handler(commands=['low_budget_movie'])
def search_lb(message: Message) -> None:
    ''' Реагирует на /low_budget_movie. Вводит пользователя в состояние получения жанра. '''

    bot.set_state(message.from_user.id, Search.genre, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Уже приступаю к поискам!!\nКстати, если хотите, чтобы я присматривала для вас кино определённого жанра, напишите мне этот жанр!\nА если нет - просто отправьте цифру \"0\"...')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how'] = 'l_budget'
        data['init'] = 'nothing'


@bot.message_handler(commands=['high_budget_movie'])
def search_hb(message: Message) -> None:
    ''' Реагирует на /high_budget_movie. Вводит пользователя в состояние получения жанра. '''

    bot.set_state(message.from_user.id, Search.genre, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Уже приступаю к поискам!!\nКстати, если хотите, чтобы я присматривала для вас кино определённого жанра, напишите мне этот жанр!\nА если нет - просто отправьте цифру \"0\"...')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['how'] = 'h_budget'
        data['init'] = 'nothing'


@bot.message_handler(state=Search.name)
def get_init(message: Message) -> None:
    ''' Когда пользователь оказывается в состоянии получения начальных данных, бот узнёт у него
     название или рейтинг фильма/сериала (в зависимости от того, что было выбрано.
     Затем бот вводит пользователя в состояние получения жанра. '''

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['how'] == 'name':
            data['init'] = message.text
            bot.set_state(message.from_user.id, Search.genre, message.chat.id)
            bot.send_message(message.from_user.id,
                             'Уже приступаю к поискам!!\nКстати, если хотите, чтобы я присматривала для вас кино определённого жанра, напишите мне этот жанр!\nА если нет - просто отправьте цифру \"0\"...')
        elif data['how'] == 'rating':
            try:
                txt = message.text
                if ',' in txt:
                    txt = txt.replace(',', '.')
                txt = float(txt)
                if 0 <= math.floor(txt) <= 10:
                    if txt >= 10:
                        txt = 10
                    data['init'] = txt
                    bot.set_state(message.from_user.id, Search.genre, message.chat.id)
                    bot.send_message(message.from_user.id,
                                     'Уже приступаю к поискам!!\nКстати, если хотите, чтобы я присматривала для вас кино определённого жанра, напишите мне этот жанр!\nА если нет - просто отправьте цифру \"0\"...')
                else:
                    bot.send_message(message.from_user.id, 'Ой! Неужели вы не знали, что рейтинг - это число от 1 до 10?..')
            except:
                bot.send_message(message.from_user.id, 'Простите, но это совсем не похоже на рейтинг...')


@bot.message_handler(state=Search.genre)
def get_genre(message: Message) -> None:
    ''' Когда пользователь оказывается в состоянии получения начальных данных, бот узнёт у него жанр фильма/сериала.
    Затем бот вводит пользователя в состояние получения кол-ва вариантов. '''


    if ',' in message.text:
        genres = message.text.split(',')
        for pos in range(len(genres)):
            if genres[pos][0] == ' ':
                genres.insert(pos, genres.pop(pos)[1:].lower())
            else:
                genres.insert(pos, genres.pop(pos).lower())
        correct = all(genre in core.GENRES for genre in genres)
        if correct:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['genre'] = genres
                data['genre_str'] = ', '.join(genres)
            bot.set_state(message.from_user.id, Search.variants, message.chat.id)
            bot.send_message(message.from_user.id,
                             'Последний маленький вопрос!\nКогда я откопаю то, что вы ищете — сколько именно результатов вам показать?')

        else:
            bot.send_message(message.from_user.id,
                             'Простите, но даже если эти жанры существуют, я о них ничего не слышала...')


    else:
        if message.text.lower() in core.GENRES:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['genre'] = message.text.lower()
                data['genre_str'] = message.text.lower()
            bot.set_state(message.from_user.id, Search.variants, message.chat.id)
            bot.send_message(message.from_user.id,
                             'Последний маленький вопрос!\nКогда я откопаю то, что вы ищете — сколько именно результатов вам показать?')

        else:
            bot.send_message(message.from_user.id,
                             'Простите, но даже если этот жанр существует, я о нём ничего не слышала...')


@bot.message_handler(state=Search.variants)
def get_variants(message: Message) -> None:
    ''' Когда пользователь оказывается в состоянии получения кол-ва вариантов, бот узнёт у него кол-во вариантов.
    Он проверяет, чтобы это количество было не слишком большим натуральным числом, затем передаёт все данные запроса в
    ф-ю search модуля database.core для поиска фильмов и получения их списка. Если хоть что-то нашлось, бот записывает
    запрос в историю запроса пользователя. Если сам пользователь ещё не существует в базе, бот его туда предварительно вносит.
    Также он передаёт данные в функцию make_list модуля keyboards.inline.usual_inline для отправки выдачи пользователю
    Затем бот вводит пользователя обратно в состояние "хаба". '''

    try:
        text = message.text
        try:
            text = int(text)
            if 0 < text < 11:
                bot.send_message(message.from_user.id,
                                 'Прекрасно! Подождите секунду, и я примчусь к вам со всем, что нашла!')
                user_id = message.from_user.id
                if User.get_or_none(User.user_id == user_id) is None:
                    User.create(
                        user_id=user_id,
                        username=message.from_user.username)
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data['id'] = message.chat.id
                    data['variants'] = text
                    data['list'] = core.search(data)
                if len(data['list']) < text:
                    bot.send_message(message.from_user.id,
                                     'Ой... Кажется, вселенная данных оказалась не такой щедрой, как хотелось бы!\nВаш запрос оказался слишком уникальным — результатов набралось лишь на скромный букетик .')
                usual_inline.make_list(data['id'], data['list'])
                if len(data['list']) != 0:
                    Request.create(
                        user_id=user_id,
                        how=data['how'],
                        genre=data['genre_str'],
                        init=data['init'],
                        vars=len(data['list']),
                        films=data['list'],
                        date=date.today()
                    )
                bot.set_state(message.from_user.id, Search.hub, message.chat.id)
            else:
                bot.send_message(message.from_user.id,
                                 'Простите, но... мои архивы не безграничны. Пожалуйста, введите число от 1 до 10 — не больше и не меньше. Иначе это будет слишком тяжело...')
        except ValueError:
            bot.send_message(message.from_user.id,
                             f'Очень смешно. Сейчас открою вам все... {text} вариантов (вот только их не существует).')
    except BaseException:
        bot.send_message(message.from_user.id,'Я ничего не смогла найти. Простите, пожалуйста...')