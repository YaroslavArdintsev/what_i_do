from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot) -> None:
    ''' Создаёт в боте базовые команды '''
    bot.set_my_commands(
        [BotCommand(i, j) for i, j in DEFAULT_COMMANDS]
    )