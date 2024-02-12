from django.template.defaultfilters import floatformat
from django.urls import reverse
from .coworkers.telegram import Telegram
from .models import TelegramBot, Coworker, Order


def send_message_via_telegram(message: str):
    for bot in TelegramBot.objects.all():
        tg = Telegram(bot.token, frozenset(chat.cid for chat in bot.chats.all() if chat.active))
        tg.send(message)


def ask_bank_for_payment_statement(order: Order, summ):
    account_id = Coworker.setting("yo", "account_id")
    secret_key = Coworker.setting("yo", "secret_key")

    data = {
        "amount": {
            "value": f"{summ:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": reverse("lms:about")  # TODO !!
        },
        "capture": False,
        "description": f"Заказ {order.uuid}",
        "metadata": {
            'orderNumber': order.uuid
        },
        "receipt": {
            "customer": {
                "full_name": order.cu_fullname,
                "email": order.cu_email,
                "phone": order.cu_phone,
            },
            "items": [
                {
                    "description": item.title,
                    "quantity": f"{item.quantity}",
                    "amount": {
                        "value": f"{item.price.amount:.2f}",
                        "currency": "RUB"
                    },
                    "vat_code": Coworker.setting("yo", "vat_code"),
                    "supplier": {
                        "name": Coworker.setting("yo", "supplier_name"),
                        "phone": Coworker.setting("yo", "supplier_phone"),
                        "inn": Coworker.setting("yo", "supplier_inn")
                    }
                } for item in order.items.all()]
        }
    }

    return str(hash(summ)), str(hash(summ))  # TODO implement me!!!!


def ask_delivery_service_for_cost(_):
    return 0  # TODO implement me!!!!
