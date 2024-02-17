from decimal import Decimal
from django.db import transaction, IntegrityError
from customerinfo.customerinfo import CustomerInfo
from lms.coworkers.yookassa import Yookassa
from lms.models import NotificationRequest, Order, OrderItem
from lms.utils import send_message_via_telegram


def create_notify_request(email, name, phone, ppk, info: CustomerInfo):
    nrq = NotificationRequest(name=name, phone=phone, email=email, ppk=ppk)
    nrq.save()
    send_message_via_telegram(str(nrq))
    info.name = name
    info.phone = phone or info.phone
    info.email = email or info.email

