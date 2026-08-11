from telegram_bot_pagination import InlineKeyboardPaginator
from loader import bot
from database import core

LISTS = {}

def make_list(user_id: int, data_list: list) -> None:
    ''' Создаёт в словаре пометку о том, какая именно выдача выдаётся пользователю и передаёт его ID в ф-ю send_films_page '''

    global LISTS
    LISTS[user_id] = data_list
    id = user_id
    send_films_page(id, 1)


def send_films_page(user_id: int, page: int = 1) -> None:
    ''' Отправляет пользователю выдачу с пагинацией '''

    try:

        paginator = InlineKeyboardPaginator(
            len(LISTS[user_id]),
            current_page=page,
            data_pattern='films#{page}'
        )


        res = LISTS[user_id][page - 1]
        text = core.show(res)
        if len('No data') < len(text) <= 1024 and res.get('poster') and res.get('poster').get('url'):
            with open(core.poster(res), 'rb') as poster:
                bot.send_photo(user_id, poster, caption=text, reply_markup=paginator.markup, parse_mode='Markdown')
        else:
            bot.send_message(user_id, text, reply_markup=paginator.markup, parse_mode='Markdown')
    except Exception:
        bot.send_message(user_id,'Я ничего не смогла найти. Простите меня, пожалуйста...')

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='films')
def films_page_callback(call):
    ''' Реагирует на нажатие кнопок, листает выдачу на ту страницу, на которую нажимает пользователь '''

    page = int(call.data.split('#')[1])
    bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_films_page(call.message.chat.id, page)