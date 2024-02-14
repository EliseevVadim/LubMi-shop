from math import radians, sin, acos, cos, fabs
from .coworkers.telegram import Telegram
from .models import TelegramBot
from functools import lru_cache


def send_message_via_telegram(message: str):
    for bot in TelegramBot.objects.all():
        tg = Telegram(bot.token, frozenset(chat.cid for chat in bot.chats.all() if chat.active))
        tg.send(message)


@lru_cache
def sph_dist(lat_0, lng_0, lat_1, lng_1, r=6371000, in_degrees=True):
    if in_degrees:
        lat_0, lng_0, lat_1, lng_1 = radians(lat_0), radians(lng_0), radians(lat_1), radians(lng_1)
    return r * acos(cos(lat_1) * cos(lat_0) * (sin(lng_1) * sin(lng_0) + cos(lng_1) * cos(lng_0)) + sin(lat_0) * sin(lat_1))


def find_nearest_city(lat, lng):  # TODO 830
    pass
