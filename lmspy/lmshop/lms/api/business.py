from customerinfo.customerinfo import CustomerInfo
from lms.models import NotificationRequest
from lms.utils import send_message_via_telegram


def create_notify_request(email, name, phone, ppk, request):
    nrq = NotificationRequest(name=name, phone=phone, email=email, ppk=ppk)
    nrq.save()
    send_message_via_telegram(str(nrq))
    info = CustomerInfo(request)
    info.name = name
    info.phone = phone or info.phone
    info.email = email or info.email
