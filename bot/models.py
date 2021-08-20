import telebot
from django.db import models


# Create your models here.
class BotConfig(models.Model):
    token = models.CharField(max_length=60, primary_key=True)
    server_url = models.CharField(max_length=100, blank=True, default='')
    is_active = models.BooleanField(default=True)

    def get_me(self):
        tbot = telebot.TeleBot(self.token)
        bot_name = tbot.get_me()
        return bot_name.username

    def set_hook(self):
        bot = telebot.TeleBot(self.token)
        webhook_url = self.server_url + '/get_hook/'
        bot.set_webhook(webhook_url)

    def save(self, *args, **kwargs):
        self.set_hook()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_me()


class IssueId(models.Model):
    id = models.BigIntegerField(primary_key=True)
