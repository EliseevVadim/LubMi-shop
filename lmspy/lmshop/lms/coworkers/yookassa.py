from enum import StrEnum
from httpx import TransportError

from lms.api.decorators import on_exception_returns
from lms.coworkers.abstractapiclient import AbstractApiClient
from lms.models import Order
from django.urls import reverse


class Yookassa(AbstractApiClient):
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
            self.setting("api_address"),
            self.setting("account_id"),
            self.setting("secret_key"))

    @property
    def key(self):
        return 'yo'

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

    @on_exception_returns((None, None, "Проблемы с созданием платежа"))
    def create_payment(self, order: Order, do_reverse_addr: bool = True):
        order_uuid = str(order.uuid)
        bj_page = f"lms:{self.setting('back_jump_page')}"
        bj_addr = f'{self.setting("back_jump_address")}{reverse(bj_page)}' if do_reverse_addr else self.setting("back_jump_address")
        res = self._post_json("payments", {"Idempotence-Key": order_uuid},
                              amount=self.amount(value=f"{order.total_price.amount:.2f}", currency="RUB"),
                              confirmation=self.confirmation(type="redirect", return_url=bj_addr),
                              capture=True,
                              description=f"Заказ #{order_uuid}",
                              metadata=self.metadata(order_uuid=order_uuid))
        return (res["id"], res["confirmation"]["confirmation_url"], None) if res["status"] == self.PaymentStatus.PENDING else (None, None, "Не удалось создать платеж")

    @on_exception_returns((PaymentStatus.UNKNOWN, None))
    def get_payment_status(self, payment_id):
        payment = self._get(f"payments/{payment_id}")
        return Yookassa.PaymentStatus(payment["status"]), payment
