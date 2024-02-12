from django.template.defaultfilters import floatformat
from django.urls import reverse
from .coworkers.telegram import Telegram
from .models import TelegramBot, Coworker, Order


def send_message_via_telegram(message: str):
    for bot in TelegramBot.objects.all():
        tg = Telegram(bot.token, frozenset(chat.cid for chat in bot.chats.all() if chat.active))
        tg.send(message)


def ask_delivery_service_for_cost(_):
    return 0  # TODO implement me!!!!
