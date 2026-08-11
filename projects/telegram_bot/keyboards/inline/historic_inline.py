from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from loader import bot
from keyboards.inline import usual_inline

LISTS = {}

def show(user_id: int, data: list) -> None:
    ''' Создаёт в словаре пометку о том, какая именно история поиска выдаётся пользователю и на
    какой странице он остановился, а также присылает ему первый эл-т истории поиска и создаёт
    инлайн-клавиатуру для переключения между страницами '''

    global LISTS
    LISTS[user_id] = [data, 1]
    markup = InlineKeyboardMarkup()
    if len(data) == 1:
        markup.add(InlineKeyboardButton(text=f'1/{len(data)}', callback_data='see'))
    else:
        markup.add(InlineKeyboardButton(text=f'1/{len(data)}', callback_data='see'), InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
    bot.send_message(user_id, data[0].string(), reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call: CallbackQuery) -> None:
    '''
    Реагирует на нажатия кнопок инлайна.
    Если нажали "назад" - листает назад, если "вперёд" - вперёд
    Если нажали на кнопку с текущей страницей, выводит выдачу по запросу на ней
    '''

    global LISTS
    req = call.data.split('_')
    user_id = call.from_user.id
    data = LISTS[user_id][0]
    page = LISTS[user_id][1]
    count = len(data)
    if req[0] == 'see':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        usual_inline.make_list(user_id, list(data[page-1].films))
    elif req[0] == 'next-page':
        page = page + 1
        markup = InlineKeyboardMarkup()
        if page < count:
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),InlineKeyboardButton(text=f'{page}/{count}', callback_data='see'),
                       InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
        else:
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),InlineKeyboardButton(text=f'{page}/{count}', callback_data='see'))
        bot.edit_message_text(data[page-1].string(), reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif req[0] == 'back-page':
        page = page - 1
        markup = InlineKeyboardMarkup()
        if page > 1:
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),InlineKeyboardButton(text=f'{page}/{count}', callback_data='see'),
                       InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
        else:
            markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data='see'),InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
        bot.edit_message_text(data[page-1].string(), reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
    LISTS[user_id][1] = page