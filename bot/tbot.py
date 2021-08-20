import telebot
from .models import BotConfig
from django.db import connection
import i18n


class TBot:
    def __init__(self):
        if 'bot_botconfig' in connection.introspection.table_names() and BotConfig.objects.filter(is_active=True):
            config = BotConfig.objects.get(is_active=True)
            self.bot = telebot.TeleBot(config.token)
        else:
            self.bot = telebot.TeleBot('123')

        i18n.load_path.append('translate')

    def update(self, json_data):
        return telebot.types.Update.de_json(json_data)
