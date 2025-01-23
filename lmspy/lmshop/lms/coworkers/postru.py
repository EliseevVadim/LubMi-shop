from decimal import Decimal
from httpx import TransportError
from lms.api.decorators import on_exception_sleep_and_retry, sleep_after, on_exception_returns
from lms.coworkers.abstractapiclient import AbstractApiClient
from lms.coworkers.dadata import DaData
from lms.coworkers.surcharges import d6y_cost_with_surcharges
from lms.models import City, Order
from lms.d6y import D6Y
from lms.utils import log_tg
from django.conf import settings


class PostRu(AbstractApiClient):
    acceptable_quality_codes = frozenset({'GOOD', 'POSTAL_BOX', 'ON_DEMAND', 'UNDEF_05'})
    acceptable_validation_codes = frozenset({'VALIDATED', 'OVERRIDDEN' 'CONFIRMED_MANUALLY'})

    def __init__(self):
        super().__init__(self.setting("api_address"), "", "")
        self._access_token = self.setting("access_token")
        self._user_auth_key = self.setting("user_auth_key")

    @property
    def key(self):
        return D6Y.PR

    @staticmethod
    def _get_postal_code(lat, lon, rad=5000.0):
        """Can throw KeyError, ValueError, TransportError or return empty result"""
        dadata = DaData()
        suggestions = dadata.pos_ru_points(DaData.location(lat=lat, lon=lon, radius_meters=rad))['suggestions']
        postal_code = next((x['data']['postal_code'] for x in suggestions
                            if 'data' in x and 'postal_code' in x['data'] and 'is_closed' in x['data'] and 'type_code' in x['data'] and
                            x['data']['type_code'].lower() not in ['почтомат', 'ти'] and not x['data']['is_closed']),
                           None)
        return postal_code or None

    @property
    def token(self):
        return self._access_token

    @property
    def user_key(self):
        return self._user_auth_key

    @property
    def authorization(self):
        return f"AccessToken {self.token}"

    @property
    def basic_auth(self):
        return None

    def compose_headers(self, content_type, headers):
        x_user_auth = {"X-User-Authorization": f"Basic {self.user_key}"} if self.user_key else {}
        cont_type = {"Content-type": "application/json;charset=UTF-8"}
        accept = {"Accept": "application/json;charset=UTF-8"}
        return super().compose_headers(content_type, headers) | x_user_auth | cont_type | accept

    def tariff(self, postal_code, price, weight):
        tf = self._post_json(
            "tariff",
            _json_={
                "delivery-point-index": postal_code,
                "index-to": postal_code,
                "declared-value": price,
                "mail-category": self.setting("mail_category"),
                "mail-type": self.setting("mail_type"),
                "mass": weight,
                "notice-payment-method": "CASHLESS",
                "payment-method": "CASHLESS",
                "transport-type": "SURFACE",
            })
        return tf

    def delivery_cost(self, dst_city_code, weight, **kwargs):
        price = Decimal(str(kwargs['price']))
        price_cents = int(round(price * 100))
        try:
            city = City.objects.get(code=dst_city_code)
        except City.DoesNotExist:
            return None, None, "Не удалось подтвердить адрес доставки"
        try:
            postal_code = self._get_postal_code(float(city.latitude), float(city.longitude))
        except (KeyError, ValueError, TransportError):
            return None, None, "Доступные отделения не найдены"
        else:
            if not postal_code:
                return None, None, "Доступные отделения не найдены"
        tariff = dict()
        try:
            tariff = self.tariff(postal_code, price_cents, weight)
            delay = tariff["delivery-time"]["min-days"] if "min-days" in tariff["delivery-time"] else tariff["delivery-time"]["max-days"]
            d6y_cost = Decimal(tariff["total-rate"] + tariff["total-vat"]) / 100
            return d6y_cost_with_surcharges(self, d6y_cost, price), delay, None
        except (KeyError, ValueError, TransportError):
            return None, None, tariff['desc'] if 'desc' in tariff else "Не удалось определить параметры доставки"

    def index_by_address(self, address: str):
        result = self._post_json("clean/address", _json_=[{"id": "0", "original-address": address}])[0]
        return result["index"] if "index" in result else None

    def poke_with_a_stick(self, region, city, street, building):
        try:
            result = self._post_json("clean/address", _json_=[{"id": "0", "original-address": f"{region}, {city}, {street}, {building}"}])[0]
            return bool("index" in result and result["index"])
        except (KeyError, ValueError, TransportError):
            return False

    def _order_as_json(self, r: Order, mail_type=None):
        """Can throw KeyError, ValueError, TransportError or return empty result"""
        index = self.index_by_address(r.delivery_address_for_posru)
        return index and {
            "address-type-to": "DEFAULT",
            "comment": f"Заказ {str(r.uuid)}",
            "completeness-checking": False,
            "courier": False,
            "delivery-to-door": False,
            "delivery-with-cod": settings.PREFERENCES.CoD(self.key),
            "fragile": False,
            "given-name": r.cu_fullname,
            "house-to": r.cu_building,
            "index-to": int(index),
            "insr-value": int(r.total_price_without_delivery.amount * 100),
            "mail-category": self.setting("mail_category"),
            "mail-direct": 643,
            "mail-type": mail_type if mail_type is not None else self.setting("mail_type"),
            "mass": r.total_weight,
            "order-num": str(r.uuid),
            "place-to": r.city.city,
            "postoffice-code": self.setting("postoffice-code", "350020"),
            "recipient-name": r.cu_fullname,
            "region-to": r.cu_city_region,
            "street-to": r.cu_street,
            "surname": r.cu_last_name,
        }

    @sleep_after()
    @on_exception_sleep_and_retry(1, (None, "Не удалось создать заказ на доставку"))
    def create_delivery_order(self, r: Order):
        if not (jsn := self._order_as_json(r)):
            raise ValueError(jsn)
        log_tg("Запрос на создание заказа на доставку:", jsn)
        result = self._put_json("user/backlog", _json_=[jsn])
        log_tg("Результат:", result)
        if "result-ids" not in result or not result["result-ids"]:
            log_tg("Запрос провален")
            raise ValueError(result)
        log_tg("Запрос успешен")
        return result, None

    @sleep_after()
    @on_exception_sleep_and_retry(1, (None, "Не удалось создать документы к заказу на доставку"))
    def create_delivery_supplements(self, r):
        @sleep_after()
        def wait():
            return None
        log_tg("Запрос на создание партии:", [r["result-ids"][0]])
        result = self._post_json("user/shipment", _json_=[r["result-ids"][0]])
        log_tg("Результат:", result)
        if "result-ids" not in result or not result["result-ids"]:
            log_tg("Запрос провален")
            raise ValueError(result)
        log_tg("Запрос успешен")
        wait()
        self._post_json(f"batch/{result['batches'][0]['batch-name']}/checkin")
        return result, None

    @sleep_after()
    @on_exception_sleep_and_retry(1, (None, "Не удалось загрузить документы к заказу на доставку"))
    def get_delivery_supplements_file(self, r, _):
        url = self.func_url(f"forms/{r['result-ids'][0]}/f7pdf")
        log_tg("Запрос на закачку транспортных документов:", f"forms/{r['result-ids'][0]}/f7pdf")
        result = self._get_file(url)
        log_tg("Результат:", result)
        if not result.is_success:
            log_tg("Запрос провален")
            raise ValueError(result.is_success)
        log_tg("Запрос успешен")
        return result.content, None

    @staticmethod
    def validate_destination(arg):
        match arg:
            case {"street": street, "building": building, "delivery_point": d6y_point} if street is not None and building is not None and d6y_point is None:
                return True
            case _:
                return False
