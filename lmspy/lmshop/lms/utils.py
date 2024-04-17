from enum import StrEnum
from math import radians, sin, acos, cos
from .coworkers.telegram import Telegram
from .models import TelegramBot, City
from functools import lru_cache
from sys import float_info
from urllib.parse import unquote


class D6Y(StrEnum):
    CD = "cd"
    PR = "pr"


def send_message_via_telegram(message: str):
    for bot in TelegramBot.objects.all():
        tg = Telegram(bot.token, frozenset(chat.cid for chat in bot.chats.all() if chat.active))
        tg.send(message)


@lru_cache
def earth_dist(lat_0, lng_0, lat_1, lng_1, er=6371000, in_degrees=True):
    if in_degrees:
        lat_0, lng_0, lat_1, lng_1 = radians(lat_0), radians(lng_0), radians(lat_1), radians(lng_1)
    return er * acos(cos(lat_0) * cos(lat_1) * cos(lng_0 - lng_1) + sin(lat_0) * sin(lat_1))


def find_nearest_city(lat, lng):
    min_dist = float_info.max
    result = None
    for city in City.objects.all():
        dist = earth_dist(lat, lng, city.latitude, city.longitude)
        if dist < min_dist:
            min_dist = dist
            result = city
    return result


def suffix(n):
    sf = "ов" if 10 < n % 100 < 20 else ["ов", "", "а", "а", "а", "ов", "ов", "ов", "ов", "ов"][n % 10]
    return sf


def clipped_range(a, b):
    if a < b:
        return [a, "-", b - 1] if b - a > 2 else [x for x in range(a, b)]
    elif b < a:
        return clipped_range(b + 1, a + 1)
    else:
        return []


def deep_unquote(s, n=10):
    r, n = unquote(s), n - 1
    return r if r == s or n < 1 else deep_unquote(r, n)