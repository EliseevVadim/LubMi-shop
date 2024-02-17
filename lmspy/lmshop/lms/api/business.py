import json
import logging

from customerinfo.customerinfo import CustomerInfo
from lms.coworkers.yookassa import Yookassa
from lms.models import NotificationRequest, Order
from lms.utils import send_message_via_telegram


def create_notify_request(email, name, phone, ppk, info: CustomerInfo):
    nrq = NotificationRequest(name=name, phone=phone, email=email, ppk=ppk)
    nrq.save()
    send_message_via_telegram(str(nrq))
    info.name = name
    info.phone = phone or info.phone
    info.email = email or info.email


def set_order_paid_by_payment(payment_id, payment):
    try:
        order = Order.pending.get(payment_id=payment_id)
    except Order.DoesNotExist:
        try:
            order = Order.objects.get(payment_id=payment_id)
            if order.status in {Order.Status.payment_paid, Order.Status.completed}:
                logging.info(f"Получено повторное подтверждение платежа {payment_id} по заказу {order.uuid}")
            else:
                logging.error(f"Получено подтверждение ранее проваленного платежа {payment_id} по заказу {order.uuid}; игнорируется!")
        except Order.DoesNotExist:
            logging.error(f"Получено подтверждение платежа {payment_id}, но соответствующий заказ не найден!")
    else:
        order.status = Order.Status.payment_paid
        order.payment_json = json.dumps(payment) if payment else None
        order.save()
        logging.info(f"Заказ {order.uuid} оплачен, платеж {payment_id} подтвержден")


def set_order_canceled_by_payment(payment_id, payment):
    try:
        order = Order.pending.get(payment_id=payment_id)
    except Order.DoesNotExist:
        try:
            order = Order.objects.get(payment_id=payment_id)
            if order.status == Order.Status.payment_canceled:
                logging.info(f"Получено повторное уведомление о провале платежа {payment_id} по заказу {order.uuid}")
            else:
                logging.error(f"Получено уведомление о провале ранее подтвержденного платежа {payment_id} по заказу {order.uuid}; игнорируется!")
        except Order.DoesNotExist:
            logging.error(f"Получено уведомление о провале платежа {payment_id}, но соответствующий заказ не найден!")
    else:
        order.status = Order.Status.payment_canceled
        order.payment_json = json.dumps(payment) if payment else None
        order.save()
        logging.info(f"Заказ {order.uuid} отменен, платеж {payment_id} провален")
        # TODO return order items back to stock !!!


def check_payment_life_cycle_is_completed(payment_id, payment_status, payment=None):
    if payment_status in Yookassa.final_payment_statuses:
        (set_order_paid_by_payment if payment_status == Yookassa.PaymentStatus.SUCCEEDED else set_order_canceled_by_payment)(payment_id, payment)
