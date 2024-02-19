from enum import StrEnum
from httpx import TransportError
from lms.coworkers.apiclient import ApiClient
from lms.models import Coworker, Order
from django.urls import reverse


class Yookassa(ApiClient):
    class PaymentStatus(StrEnum):
        PENDING = "pending"
        WAITING_FOR_CAPTURE = "waiting_for_capture"
        SUCCEEDED = "succeeded"
        CANCELED = "canceled"
        UNKNOWN = "unknown"

    final_payment_statuses = frozenset((PaymentStatus.SUCCEEDED, PaymentStatus.CANCELED))
    transient_payment_statuses = frozenset((PaymentStatus.PENDING, PaymentStatus.UNKNOWN))
    payment_statuses_are_notification_subjects = final_payment_statuses | {PaymentStatus.UNKNOWN}

    def __init__(self):
        super().__init__(
            "yo",
            Coworker.setting("yo", "api_address"),
            Coworker.setting("yo", "account_id"),
            Coworker.setting("yo", "secret_key"))

    @staticmethod
    def amount(**kwargs):
        return Yookassa._construct_arg_({
            "value": (str, None),  # -- Сумма
            "currency": (str, Yookassa._max_len_(3)),  # -- Валюта
        }, **kwargs)

    @staticmethod
    def confirmation(**kwargs):
        return Yookassa._construct_arg_({
            "type": (str, Yookassa._one_of_("redirect")),  # -- Тип
            "return_url": (str, None),  # -- Адрес
        }, **kwargs)

    @staticmethod
    def metadata(**kwargs):
        return Yookassa._construct_arg_({
            "order_uuid": (str, Yookassa._uuid_()),  # -- UUID ордера
        }, **kwargs)

    def create_payment(self, order: Order, summ):
        order_uuid = str(order.uuid)
        back_page = f"lms:{self.setting('back_jump_page')}"
        bad_result = None, None, "Проблемы с созданием платежа"
        try:
            res = self._post_json("payments", {"Idempotence-Key": order_uuid}, amount=Yookassa.amount(value=f"{summ:.2f}", currency="RUB"),
                                  confirmation=Yookassa.confirmation(type="redirect", return_url=f'{self.setting("back_jump_address")}{reverse(back_page)}'), capture=True,
                                  description=f"Заказ #{order_uuid}", metadata=Yookassa.metadata(order_uuid=order_uuid))
        except TransportError:
            return bad_result
        try:
            return (res["id"], res["confirmation"]["confirmation_url"], None) if res["status"] == Yookassa.PaymentStatus.PENDING else bad_result
        except KeyError:
            return bad_result

    def get_payment_status(self, payment_id):
        try:
            payment = self._get(f"payments/{payment_id}")
        except TransportError:
            return Yookassa.PaymentStatus.UNKNOWN, None
        try:
            return Yookassa.PaymentStatus(payment["status"]), payment
        except (KeyError, ValueError):
            return Yookassa.PaymentStatus.UNKNOWN, None
