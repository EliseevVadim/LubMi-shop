import logging
from enum import StrEnum
from uuid import UUID
from django.http import HttpResponse
from django.conf import settings
from lms.api.decorators import on_exception_returns
from lms.coworkers.abstractapiclient import AbstractApiClient
from lms.models import Order
from hashlib import sha256
from lms.utils import log_tg


class TBank(AbstractApiClient):
    class PaymentStatus(StrEnum):
        NEW = "NEW"  # MAPI получил запрос Init. После этого, он создает новый платеж в статусе NEW и возвращает обратно его идентификатор в параметре PaymentId и ссылку на платежную форму в параметре PaymentURL
        FORM_SHOWED = "FORM_SHOWED"  # Мерчант перенаправил клиента на страницу платежной формы PaymentURL и страница загрузилась у клиента в браузере
        AUTHORIZING = "AUTHORIZING"  # Платеж обрабатывается MAPI и платежной системой
        TDS_CHECKING = "3DS_CHECKING"  # Платеж проходит проверку 3D-Secure
        TDS_CHECKED = "3DS_CHECKED"  # Платеж успешно прошел проверку 3D-Secure
        AUTHORIZED = "AUTHORIZED"  # Платеж авторизован, деньги заблокированы на карте клиента
        CONFIRMING = "CONFIRMING"  # Подтверждение платежа обрабатывается MAPI и платежной системой
        CONFIRMED = "CONFIRMED"  # Платеж подтвержден, деньги списаны с карты клиента
        REVERSING = "REVERSING"  # Мерчант запросил отмену авторизованного, но еще не подтвержденного платежа. Возврат обрабатывается MAPI и платежной системой
        PARTIAL_REVERSED = "PARTIAL_REVERSED"  # Частичный возврат по авторизованному платежу завершился успешно
        REVERSED = "REVERSED"  # Полный возврат по авторизованному платежу завершился успешно
        REFUNDING = "REFUNDING"  # Мерчант запросил отмену подтвержденного платежа. Возврат обрабатывается MAPI и платежной системой
        PARTIAL_REFUNDED = "PARTIAL_REFUNDED"  # Частичный возврат по подтвержденному платежу завершился успешно
        REFUNDED = "REFUNDED"  # Полный возврат по подтвержденному платежу завершился успешно
        CANCELED = "CANCELED"  # Мерчант отменил платеж
        DEADLINE_EXPIRED = "DEADLINE_EXPIRED"  # 1. Клиент не завершил платеж в срок жизни ссылки на платежную форму PaymentURL. Этот срок Мерчант настраивает в Личном кабинете, либо передает в параметре RedirectDueDate при вызове метода Init 2. Платеж не прошел проверку 3D-Secure в срок
        REJECTED = "REJECTED"  # Банк отклонил платеж
        AUTH_FAIL = "AUTH_FAIL"  # Платеж завершился ошибкой или не прошел проверку 3D-Secure
        UNKNOWN = "UNKNOWN"  # Не удалось проверить статус платежа

    final_payment_statuses = frozenset((PaymentStatus.CONFIRMED, PaymentStatus.CANCELED, PaymentStatus.DEADLINE_EXPIRED, PaymentStatus.REJECTED, PaymentStatus.AUTH_FAIL))
    considerable_types = frozenset({bool, int, float, str})
    token_key = 'Token'
    notification_response_good = HttpResponse('OK')
    notification_response_bad = HttpResponse(content='', status=404)
    max_desc_len = 140

    def __init__(self):
        super().__init__(
            self.setting("api_address"),
            self.setting("terminal_key"),
            self.setting("terminal_secret"))

    @property
    def key(self):
        return 'tb'

    @property
    def terminal_key(self):
        return self.client_id

    @property
    def terminal_password(self):
        return self.client_secret

    @property
    def access_token(self):
        return self.setting("access_token")

    @property
    def authorization(self):
        return f"Bearer {self.access_token}"

    @staticmethod
    def _signature(data: dict, password: str):
        filter = lambda k, v: type(k) is str and k != TBank.token_key and type(v) in TBank.considerable_types
        convert = lambda v: v if type(v) is not bool else ('false', 'true')[v]
        values = {'Password': password} | {k: convert(v) for k, v in data.items() if filter(k, v)}
        return sha256(bytearray("".join(f"{values[k]}" for k in sorted(values.keys())), 'utf-8')).hexdigest()

    def _sign(self, data: dict, password: str):
        data[self.token_key] = self._signature(data, password)
        return data

    def _prepare_json(self, json):
        return self._sign(json, self.terminal_password)

    def check_signature(self, data: dict):
        if self._signature(data, self.terminal_password) != data[self.token_key]:
            logging.warning(f'Проверка подписи провалена: {data}')
            raise ValueError(data)

    @staticmethod
    def pid2uuid(pid: str) -> str:
        return str(UUID(int=int(pid)))

    @staticmethod
    def uuid2pid(uuid: str) -> str:
        return str(UUID(uuid).int)

    @on_exception_returns((None, None, 'Проблемы с созданием платежа'))
    def create_payment(self, order: Order):
        opt = lambda **kwargs: {k: v for k, v in kwargs.items() if v is not None}
        order_uuid = str(order.uuid)
        log_tg("Запрос на создание платежа для заказа", order_uuid)
        result = self._post_json('Init', {},
                                 TerminalKey=self.terminal_key,
                                 Amount=int(order.total_price.amount * 100),
                                 OrderId=order_uuid,
                                 Description=self.setting('payment-description', 'Заказ в онлайн-магазине одежды LubMi')[:self.max_desc_len],
                                 PayType='O',
                                 **opt(NotificationURL=self.setting('notification-url'),
                                       SuccessURL=self.setting('success-url'),
                                       FailURL=self.setting('fail-url')),
                                 DATA={
                                     'OperationInitiatorType': int(self.setting('operation-initiator-type', '0'))},
                                 Receipt=opt(Email=order.cu_email, Phone=order.cu_phone) | {
                                     'Taxation': self.setting('taxation', 'usn_income'),
                                     'Items': [{
                                         'Name': item.title,
                                         'Price': item.price_cents,
                                         'Quantity': item.quantity,
                                         'Amount': item.amount_cents,
                                         'PaymentMethod': self.setting('payment-method', 'full_prepayment'),
                                         'PaymentObject': self.setting('goods-payment-object', 'commodity'),
                                         'Tax': self.setting('goods-tax', 'none'),
                                     } for item in order.items.all()] + ([{
                                         'Name': 'Доставка',
                                         'Price': order.delivery_cost_cents,
                                         'Quantity': 1,
                                         'Amount': order.delivery_cost_cents,
                                         'PaymentMethod': self.setting('payment-method', 'full_prepayment'),
                                         'PaymentObject': self.setting('service-payment-object', 'service'),
                                         'Tax': self.setting('service-tax', 'none')}] if not settings.PREFERENCES.CashOnD6y else [])})
        log_tg("Результат:", result)
        if result['Success']:
            log_tg("Запрос успешен")
            return self.pid2uuid(result['PaymentId']), result['PaymentURL'], None
        log_tg("Запрос провален")
        raise ValueError(result)

    @on_exception_returns((PaymentStatus.UNKNOWN, None))
    def get_payment_status(self, payment_id):
        info = self._post_json('GetState', {},
                               TerminalKey=self.terminal_key,
                               PaymentId=self.uuid2pid(payment_id))
        if info['Success']:
            return info['Status'], info
        raise ValueError(info)
