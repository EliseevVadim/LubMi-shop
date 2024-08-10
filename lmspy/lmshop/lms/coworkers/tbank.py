import logging
from enum import StrEnum
from uuid import UUID
from lms.api.decorators import on_exception_returns
from lms.coworkers.abstractapiclient import AbstractApiClient
from lms.models import Order
from hashlib import sha256


class TBank(AbstractApiClient):
    class PaymentStatus(StrEnum):
        NEW = "NEW"                             # MAPI получил запрос Init. После этого, он создает новый платеж в статусе NEW и возвращает обратно его идентификатор в параметре PaymentId и ссылку на платежную форму в параметре PaymentURL
        FORM_SHOWED = "FORM_SHOWED"             # Мерчант перенаправил клиента на страницу платежной формы PaymentURL и страница загрузилась у клиента в браузере
        AUTHORIZING = "AUTHORIZING"             # Платеж обрабатывается MAPI и платежной системой
        TDS_CHECKING = "3DS_CHECKING"           # Платеж проходит проверку 3D-Secure
        TDS_CHECKED = "3DS_CHECKED"             # Платеж успешно прошел проверку 3D-Secure
        AUTHORIZED = "AUTHORIZED"               # Платеж авторизован, деньги заблокированы на карте клиента
        CONFIRMING = "CONFIRMING"               # Подтверждение платежа обрабатывается MAPI и платежной системой
        CONFIRMED = "CONFIRMED"                 # Платеж подтвержден, деньги списаны с карты клиента
        REVERSING = "REVERSING"                 # Мерчант запросил отмену авторизованного, но еще не подтвержденного платежа. Возврат обрабатывается MAPI и платежной системой
        PARTIAL_REVERSED = "PARTIAL_REVERSED"   # Частичный возврат по авторизованному платежу завершился успешно
        REVERSED = "REVERSED"                   # Полный возврат по авторизованному платежу завершился успешно
        REFUNDING = "REFUNDING"                 # Мерчант запросил отмену подтвержденного платежа. Возврат обрабатывается MAPI и платежной системой
        PARTIAL_REFUNDED = "PARTIAL_REFUNDED"   # Частичный возврат по подтвержденному платежу завершился успешно
        REFUNDED = "REFUNDED"                   # Полный возврат по подтвержденному платежу завершился успешно
        CANCELED = "CANCELED"                   # Мерчант отменил платеж
        DEADLINE_EXPIRED = "DEADLINE_EXPIRED"   # 1. Клиент не завершил платеж в срок жизни ссылки на платежную форму PaymentURL. Этот срок Мерчант настраивает в Личном кабинете, либо передает в параметре RedirectDueDate при вызове метода Init 2. Платеж не прошел проверку 3D-Secure в срок
        REJECTED = "REJECTED"                   # Банк отклонил платеж
        AUTH_FAIL = "AUTH_FAIL"                 # Платеж завершился ошибкой или не прошел проверку 3D-Secure
        UNKNOWN = "UNKNOWN"                     # Не удалось проверить статус платежа

    final_payment_statuses = frozenset((PaymentStatus.CONFIRMED, PaymentStatus.CANCELED, PaymentStatus.DEADLINE_EXPIRED, PaymentStatus.REJECTED, PaymentStatus.AUTH_FAIL))
    sign_types = frozenset({bool, int, float, str})

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
        condition = lambda k, v: type(k) is str and k != 'Token' and type(v) in TBank.sign_types
        convert = lambda v: v if type(v) is not bool else ('false', 'true')[v]
        values = {'Password': password} | {k: convert(v) for k, v in data.items() if condition(k, v)}
        return sha256(bytearray("".join(f"{values[k]}" for k in sorted(values.keys())), 'utf-8')).hexdigest()

    def _sign(self, data: dict, password: str):
        data['Token'] = self._signature(data, password)
        return data

    def _prepare_json(self, json):
        return self._sign(json, self.terminal_password)

    def check(self, data: dict):
        if self._signature(data, self.terminal_password) != data['Token']:
            logging.warning(f'Проверка подписи провалена: {data}')
            raise ValueError(data)

    @staticmethod
    def pid2uuid(pid: str) -> str:
        return str(UUID(int=int(pid)))

    @staticmethod
    def uuid2pid(ip: str) -> str:
        return str(UUID(ip).int)

    @on_exception_returns((None, None, 'Проблемы с созданием платежа'))
    def create_payment(self, order: Order, summ, *args):
        order_uuid = str(order.uuid)
        res = self._post_json('Init', {},
                              TerminalKey=self.terminal_key,
                              Amount=int(summ * 100),
                              OrderId=order_uuid,
                              Description=f'Заказ #{order_uuid}',
                              PayType='O',
                              DATA={'OperationInitiatorType': 0})
        if res['Success']:
            return self.pid2uuid(res['PaymentId']), res['PaymentURL'], None
        raise ValueError(res)

    @on_exception_returns((PaymentStatus.UNKNOWN, None))
    def get_payment_status(self, payment_id):
        info = self._post_json('GetState', {},
                               TerminalKey=self.terminal_key,
                               PaymentId=self.uuid2pid(payment_id))
        if info['Success']:
            return info['Status'], info
        raise ValueError(info)
