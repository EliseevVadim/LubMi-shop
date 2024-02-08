import httpx
import re
import functools

from lms.deco import copy_result, singleton
from lms.models import Coworker
from urllib.parse import quote
from datetime import datetime
from threading import Lock


@singleton
class Cdek:
    uuid_re = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$")

    @staticmethod
    def setting(name):
        return Coworker.setting("cd", name)

    def __init__(self,
                 address=setting("api_address"),
                 client_id=setting("client_id"),
                 client_secret=setting("client_secret")):
        self._address = address
        self._client_id = client_id
        self._client_secret = client_secret
        self._lock_auth = Lock()
        self._auth = self._tp_auth = None

    @staticmethod
    def _quoted(kwargs):
        return {quote(str(k)): quote(str(v)) for k, v in kwargs.items()}

    @property
    @copy_result
    def auth(self):
        def ask_auth():
            with httpx.Client() as client:
                self._auth = client.post(
                    f"{self._address}/oauth/token?parameters",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "client_credentials",
                        "client_id": quote(self._client_id),
                        "client_secret": quote(self._client_secret)
                    }
                ).json()
                self._tp_auth = datetime.now()
                return self._auth

        def auth_alive():
            return self._auth and self._tp_auth and 5 + (datetime.now() - self._tp_auth).seconds < self._auth["expires_in"]

        with self._lock_auth:
            return self._auth if auth_alive() else ask_auth()

    def _post(self, func, **kwargs):
        with httpx.Client() as client:
            result = client.post(
                f"{self._address}/{func}",
                headers={
                    "Authorization": f"{self.token_type} {self.access_token}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data=Cdek._quoted(kwargs)
            ).json()
            return result

    def _post_json(self, func, **kwargs):
        with httpx.Client() as client:
            result = client.post(
                f"{self._address}/{func}",
                headers={
                    "Authorization": f"{self.token_type} {self.access_token}",
                    "Content-Type": "application/json"
                },
                json=kwargs
            ).json()
            return result

    def _get(self, func, **kwargs):
        with httpx.Client() as client:
            result = client.get(
                f"{self._address}/{func}",
                headers={
                    "Authorization": f"{self.token_type} {self.access_token}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                params=Cdek._quoted(kwargs)
            ).json()
            return result

    @staticmethod
    # @functools.lru_cache
    def _construct_(decl: dict[str, tuple], **kwargs):
        var = {}
        for k, v in kwargs.items():
            d = decl[k]
            if type(v) is not d[0]:
                raise TypeError(v)
            if d[1] and not d[1](v):
                raise ValueError(v)
            var[k] = v
        return var

    @staticmethod
    @functools.lru_cache
    def _max_len_(n):
        return lambda v: len(v) <= n

    @staticmethod
    @functools.lru_cache
    def _positive_():
        return lambda v: v > 0

    @staticmethod
    @functools.lru_cache
    def _no_negative_():
        return lambda v: v > 0

    @staticmethod
    @functools.lru_cache
    def _country_code_():
        return Cdek._max_len_(2)

    @staticmethod
    @functools.lru_cache
    def _str_255_():
        return Cdek._max_len_(255)

    @staticmethod
    @functools.lru_cache
    def _uuid_():
        return lambda v: bool(Cdek.uuid_re.match(v))

    @staticmethod
    @functools.lru_cache
    def _one_of_(*args):
        return lambda v: v in frozenset(args)

    @auth.deleter
    def auth(self):
        with self._lock_auth:
            self._auth = self._tp_auth = None

    @property
    def access_token(self):
        return self.auth["access_token"]

    @property
    def token_type(self):
        return self.auth["token_type"]

    @property
    def auth_expires(self):
        return self.auth["expires_in"]

    @property
    def auth_scope(self):
        return self.auth["scope"]

    @property
    def jti(self):
        return self.auth["jti"]

    @staticmethod
    def location(**kwargs):
        return Cdek._construct_({
            "code": (int, None),                            # -- Код населенного пункта, integer
            "fias_guid": (str, Cdek._uuid_()),              # -- Уникальный идентификатор ФИАС, UUID
            "postal_code": (str, Cdek._str_255_()),         # -- Почтовый индекс, string(255)
            "longitude": (float, None),                     # -- Долгота, float
            "latitude": (float, None),                      # -- Широта, float
            "country_code": (str, Cdek._country_code_()),   # -- Код страны в формате ISO_3166-1_alpha-2, string(2)
            "region": (str, Cdek._str_255_()),              # -- Название региона, string(255)
            "sub_region": (str, Cdek._str_255_()),          # -- Название района региона, string(255)
            "city": (str, Cdek._str_255_()),                # -- Название города, string(255)
            "address": (str, Cdek._str_255_())              # -- Строка адреса, string(255)
        }, **kwargs)

    @staticmethod
    def service(**kwargs):
        return Cdek._construct_({
            "code": (int, None),                            # -- Код дополнительной услуги, integer
            "parameter": (str, None),                       # -- Параметр дополнительной услуги, string
        }, **kwargs)

    @staticmethod
    def package(**kwargs):
        return Cdek._construct_({
            "number": (str, Cdek._str_255_()),      # -- Номер упаковки, string(255)
            "weight": (int, Cdek._positive_()),     # -- Общий вес (в граммах), integer
            "length": (int, Cdek._positive_()),     # -- Габариты упаковки. Длина (в сантиметрах), integer
            "width": (int, Cdek._positive_()),      # -- Габариты упаковки. Ширина (в сантиметрах), integer
            "height": (int, Cdek._positive_()),     # -- Габариты упаковки. Высота (в сантиметрах), integer
            "comment": (str, Cdek._str_255_()),     # -- Комментарий к упаковке, string(255)
            "items": (list, None),                  # -- Позиции товаров в упаковке, item[]
        }, **kwargs)

    @staticmethod
    def item(**kwargs):
        return Cdek._construct_({
            "name": (str, Cdek._str_255_()),                # -- Наименование товара (может также содержать описание товара: размер, цвет), string(255)
            "ware_key": (str, Cdek. _max_len_(20)),	        # -- Идентификатор/артикул товара, string(20)
            "payment": (dict, None),	                    # -- Оплата за товар при получении (за единицу товара в указанной валюте, значение >=0) — наложенный платеж, в случае предоплаты значение = 0, money
            "cost": (float, Cdek._no_negative_()),	        # -- Объявленная стоимость товара (за единицу товара в указанной валюте, значение >=0). С данного значения рассчитывается страховка, float
            "weight": (int, Cdek._positive_()),	            # -- Вес (за единицу товара, в граммах), integer
            "weight_gross": (int, Cdek._positive_()),       # -- Вес брутто, integer
            "amount": (int, Cdek._positive_()),	            # -- Количество единиц товара (в штуках), integer
            "name_i18n": (str, Cdek._str_255_()),	        # -- Наименование на иностранном языке	string(255)
            "brand": (str, Cdek._str_255_()),               # -- Бренд на иностранном языке, string(255)
            "country_code": (str, Cdek._country_code_()),   # -- Код страны в формате  ISO_3166-1_alpha-2, string(2)
            "material": (str, Cdek._str_255_()),            # -- Код материала, string(255)
            "wifi_gsm": (bool, None),                       # -- Содержит wifi/gsm, boolean
            "url": (str, Cdek._str_255_()),	                # -- Ссылка на сайт интернет-магазина с описанием товара, string(255)
        }, **kwargs)

    @staticmethod
    def money(**kwargs):
        return Cdek._construct_({
            "value": (float, Cdek._no_negative_()),	            # -- Сумма в валюте, float
            "vat_sum": (float, Cdek._no_negative_()),	        # -- Сумма НДС, float
            "vat_rate": (int, Cdek._one_of_(0, 10, 12, 20)),    # -- Ставка НДС (значение - 0, 10, 12, 20, null - нет НДС)
        }, **kwargs)

    def cities(self, country_codes: str = "RU", **kwargs):
        return self._get("location/cities", country_codes=country_codes, **kwargs)

    def regions(self, country_codes: str = "RU", **kwargs):
        return self._get("location/regions", country_codes=country_codes, **kwargs)

    def points(self, country_codes: str = "RU", **kwargs):
        return self._get("deliverypoints", country_codes=country_codes, **kwargs)

    def tariff(self,
               tariff_code,         # -- Код тарифа, integer --
               from_location,       # -- Адрес отправления, location --
               to_location,         # -- Адрес получения, location --
               packages,            # -- Список информации по местам (упаковкам), package[] --
               services,            # -- Дополнительные услуги, service[] --
               **kwargs):
        return self._post_json("calculator/tariff",
                               tariff_code=tariff_code,
                               from_location=from_location,
                               to_location=to_location,
                               packages=packages,
                               services=services,
                               **kwargs)

    def tariff_list(self,
                    from_location,  # -- Адрес отправления, location --
                    to_location,    # -- Адрес получения, location --
                    packages,       # -- Список информации по местам (упаковкам), package[] --
                    **kwargs):
        return self._post_json("calculator/tarifflist",
                               from_location=from_location,
                               to_location=to_location,
                               packages=packages,
                               **kwargs)


cdek_delivery = Cdek()
