import json
import logging
from threading import Thread
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from customerinfo.customerinfo import CustomerInfo
from lms.coworkers.tbank import TBank
from lms.coworkers.yookassa import Yookassa
from lms.models import NotificationRequest, Order, AvailableSize
from lms.utils import send_message_via_telegram, log_tg
from lms.d6y_factory import ds_factory


def create_notify_request(email, phone, ppk, size, info: CustomerInfo):
    nrq = NotificationRequest(name=info.short_name or "Не указано", phone=phone, email=email, ppk=ppk, size=size)
    nrq.save()
    send_message_via_telegram(str(nrq))
    info.phone = phone or info.phone
    info.email = email or info.email


def ensure_order_delivery_supplements_exist(order_id):
    try:
        order = Order.paid.get(slug=order_id)
    except Order.DoesNotExist:
        return f"Заказ {order_id} не найден"

    if order.status != Order.Status.payment_paid:
        return "Недопустимый статус заказа"
    ds = ds_factory(order.delivery_service)
    if not order.delivery_order_json:
        dvo, error = ds.create_delivery_order(order, logger=log_tg)  # TODO kill logger
        if not dvo or error:
            return error or "Не удалось создать заказ"
        order.delivery_order_json = json.dumps(dvo)
        order.save()
    else:
        dvo = json.loads(order.delivery_order_json)

    if not order.delivery_supplements_json:
        dvs, error = ds.create_delivery_supplements(dvo, logger=log_tg)  # TODO kill logger
        if not dvs or error:
            return error or "Не удалось создать файл с транспортной документацией"
        order.delivery_supplements_json = json.dumps(dvs)
        order.save()
    else:
        dvs = json.loads(order.delivery_supplements_json)

    if not order.delivery_supplements_file:
        file, error = ds.get_delivery_supplements_file(dvo, dvs, logger=log_tg)  # TODO kill logger
        if not file or error:
            return error or "Не удалось загрузить файл с транспортной документацией"
        order.delivery_supplements_file = file
        order.save()
    return None


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
        link1: str = settings.ADMIN_DOMAIN + reverse('lms:admin_order_details', args=[order.slug])
        link2: str = settings.ADMIN_DOMAIN + reverse('lms:admin_order_delivery_documents', args=[order.slug])
        items: str = '\n'.join(f'– Артикул, название: `{i.title}`, Цвет: `{i.color}`, Размер: `{i.size}`, Количество: `{i.quantity}`, Цена: `{i.price}`, Вес: `{i.weight}`' for i in order.items.all())
        message: str = f"""Заказ [{order.uuid}]({link1})
Статус: `оплачен`
Заказчик: `{order.cu_fullname}`
Служба доставки: `{order.DeliveryService[order.delivery_service].label}`
Адрес доставки: `{order.delivery_address}`
Платеж: `{payment_id}`\n
Позиции по заказу:
{items}\n
Стоимость доставки: `{order.delivery_cost}`
Полная стоимость заказа: `{order.total_price}`
Детали заказа: [Перейти]({link1})
Транспортные документы: [Скачать]({link2})"""
        send_message_via_telegram(message)
        logging.info(f"Заказ {order.uuid} оплачен, платеж {payment_id} подтвержден")
        if settings.D6Y_SUPPLEMENTS_IMMEDIATELY:
            th = Thread(target=ensure_order_delivery_supplements_exist, args=(order.slug,), daemon=True)
            th.start()


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
        unbind_order_products(order)
        logging.info(f"Заказ {order.uuid} отменен, платеж {payment_id} провален")


def set_order_completed(order_id, by_slug=False):
    try:
        order = Order.paid.get(slug=order_id) if by_slug else Order.paid.get(pk=order_id)
    except Order.DoesNotExist:
        logging.warning(f"Заказ {order_id} не найден при попытке закрыть его; игнорируется!")
    else:
        order.status = Order.Status.completed
        order.completed_at = timezone.now()
        order.save()
        unbind_order_products(order)
        logging.info(f"Заказ {order.uuid} закрыт")


def unbind_order_products(order: Order):
    for item in order.items.all():
        if order.status == Order.Status.payment_canceled:
            try:
                size = item.product.sizes.get(size=item.size)
                size.quantity += item.quantity
                size.save()
            except AvailableSize.DoesNotExist:
                size = AvailableSize(product=item.product, size=item.size, quantity=item.quantity)
                size.save()
        item.product = None
        item.save()


def yo__check_payment_life_cycle_is_completed(payment_id, payment_status, payment=None):
    if payment_status in Yookassa.final_payment_statuses:
        (set_order_paid_by_payment if payment_status == Yookassa.PaymentStatus.SUCCEEDED else set_order_canceled_by_payment)(payment_id, payment)


def tb__check_payment_life_cycle_is_completed(payment_id, payment_status, payment=None):
    if payment_status in TBank.final_payment_statuses:
        (set_order_paid_by_payment if payment_status == TBank.PaymentStatus.CONFIRMED else set_order_canceled_by_payment)(payment_id, payment)



