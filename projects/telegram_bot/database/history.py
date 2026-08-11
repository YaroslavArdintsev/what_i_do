from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField, IntegrityError, State, \
    TextField, DateField
import json

db = SqliteDatabase("database/users.db")
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]


class BaseModel(Model):
    ''' Базовый класс, от которого будут наследовать все модели '''

    class Meta:
        database = db


class User(BaseModel):
    ''' Класс пользователя, характеризующийся ID и списком запросов '''

    user_id = IntegerField(primary_key=True)


class ListField(TextField):
    ''' Специальное поле, в котором можно будет хранить списки (нужно для сохранения истории запросов) '''

    def db_value(self, value):
        if value is None:
            return '[]'
        return json.dumps(value)

    def python_value(self, value):
        if value is None:
            return []
        return json.loads(value)


class Request(BaseModel):
    '''
    Класс запроса, характеризующийся:

    1) собственным ID
    2) ID пользователя
    3) способом поиска
    4) изначальными данными фильма (названием/рейтингом)
    5) жанром фильма
    6) количеством результатов в выдаче
    7) выдачей (списком фильмов)
    8) датой запроса
    '''

    request_id = AutoField()
    user_id = ForeignKeyField(User, backref="requests")
    how = CharField()
    init = CharField(null=True)
    genre = CharField()
    vars = IntegerField()
    films = ListField(default=list)
    date = DateField()

    def string(self) -> str:
        ''' Превращает запрос в его текстовое описание '''
        date = str(self.date).split('-')
        month = int(date[1])
        advice = '\n\nЧтобы увидеть список фильмов по вашему запросу, нажмите на кнопку с номером страницы.'
        if self.genre == '0':
            genre = 'не указан'
        else:
            genre = self.genre
        if self.how == 'name':
            return f'{date[2]} {MONTHS[month-1]} {date[0]}\nПоиск по названию\n\nНазвание: {self.init}\nЖанр: {genre}\nКоличество найденных фильмов: {self.vars}{advice}'
        elif self.how == 'rating':
            return f'{date[2]} {MONTHS[month-1]} {date[0]}\nПоиск по рейтингу\n\nРейтинг: {self.init}\nЖанр: {genre}\nКоличество найденных фильмов: {self.vars}{advice}'
        elif self.how == 'h_budget':
            return f'{date[2]} {MONTHS[month-1]} {date[0]}\nПоиск высокобюджетных фильмов\n\nЖанр: {genre}\nКоличество найденных фильмов: {self.vars}{advice}'
        elif self.how == 'l_budget':
            return f'{date[2]} {MONTHS[month-1]} {date[0]}\nПоиск низкобюджетных фильмов\n\nЖанр: {genre}\nКоличество найденных фильмов: {self.vars}{advice}'


def create_models() -> None:
    ''' Создаёт таблицы пользователей и запросов '''
    db.create_tables(BaseModel.__subclasses__())


create_models()