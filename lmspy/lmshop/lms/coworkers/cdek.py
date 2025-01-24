from decimal import Decimal
import httpx
from httpx import TransportError
from lms.api.decorators import on_exception_sleep_and_retry, sleep_after
from lms.coworkers.abstractapiclient import AbstractApiClient
from lms.coworkers.surcharges import d6y_cost_with_surcharges
from lms.deco import copy_result
from lms.models import Coworker, Order, Parameter
from urllib.parse import quote
from django.core.cache import cache
from django.conf import settings
from lms.d6y import D6Y
from lms.utils import log_tg


class Cdek(AbstractApiClient):
    def __init__(self):
        super().__init__(self.setting("api_address"),
                         self.setting("client_id"),
                         self.setting("client_secret"))

    @property
    def key(self):
        return D6Y.CD

    @property
    @copy_result
    def auth(self):
        def ask_auth():
            with httpx.Client() as client:
                return client.post(
                    f"{self.address}/oauth/token?parameters",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "client_credentials",
                        "client_id": quote(self.client_id),
                        "client_secret": quote(self.client_secret)
                    }
                ).json()
        auth_ = cache.get("cdek-auth")
        if auth_ is None:
            auth_ = ask_auth()
            cache.set("cdek-auth", auth_, int(auth_["expires_in"]) - 5)
        return auth_

    @property
    def authorization(self):
        return f"{self.token_type} {self.access_token}"

    @property
    def basic_auth(self):
        return None

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

    @property
    def stickers_type(self):
        return self.setting("stickers_type", "orders")

    @staticmethod
    def extract_error(response):
        errs = (er["message"] for er in response["errors"]) if "errors" in response else None
        return '; '.join(errs) if errs else "Неизвестная ошибка"

    @staticmethod
    def location(**kwargs):
        return Cdek._construct_arg_({
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
        return Cdek._construct_arg_({
            "code": (int, None),                            # -- Код дополнительной услуги, integer
            "parameter": (str, None),                       # -- Параметр дополнительной услуги, string
        }, **kwargs)

    @staticmethod
    def package(**kwargs):
        return Cdek._construct_arg_({
            "number": (str, Cdek._max_len_(30)),    # -- Номер упаковки, string(255)
            "weight": (int, Cdek._positive_()),     # -- Общий вес (в граммах), integer
            "length": (int, Cdek._positive_()),     # -- Габариты упаковки. Длина (в сантиметрах), integer
            "width": (int, Cdek._positive_()),      # -- Габариты упаковки. Ширина (в сантиметрах), integer
            "height": (int, Cdek._positive_()),     # -- Габариты упаковки. Высота (в сантиметрах), integer
            "comment": (str, Cdek._str_255_()),     # -- Комментарий к упаковке, string(255)
            "items": (list, None),                  # -- Позиции товаров в упаковке, item[]
        }, **kwargs)

    @staticmethod
    def item(**kwargs):
        return Cdek._construct_arg_({
            "name": (str, Cdek._str_255_()),                # -- Наименование товара (может также содержать описание товара: размер, цвет), string(255)
            "ware_key": (str, Cdek. _max_len_(50)),	        # -- Идентификатор/артикул товара, string(20)
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
        return Cdek._construct_arg_({
            "value": (float, Cdek._no_negative_()),	                  # -- Сумма в валюте, float
            "vat_sum": (float, Cdek._no_negative_()),	              # -- Сумма НДС, float
            "vat_rate": (int, Cdek._one_of_(0, 10, 12, 20)),    # -- Ставка НДС (значение - 0, 10, 12, 20, null - нет НДС)
        }, **kwargs)

    @staticmethod
    def phone(**kwargs):
        return Cdek._construct_arg_({
            "number": (str, Cdek._str_255_()),      # -- номер
            "additional": (str, Cdek._str_255_()),  # -- некая фигня
        }, **kwargs)

    @staticmethod
    def recipient(**kwargs):
        return Cdek._construct_arg_({
            "name": (str, Cdek._str_255_()),                        # -- ФИО --
            "passport_series": (str, Cdek. _max_len_(4)),           # -- Серия паспорта    string(4)    нет
            "passport_number": (str, Cdek. _max_len_(30)),          # -- Номер паспорта    string(30)    нет
            "passport_date_of_issue": (str, Cdek._max_len_(10)),    # -- Дата выдачи паспорта    date(yyyy - MM - dd)    нет
            "passport_organization": (str, Cdek. _str_255_()),      # -- Орган выдачи паспорта    string(255)    нет
            "tin": (str, Cdek._max_len_(12)),                       # -- ИНН Может содержать 10, либо 12 символов                 string(12)    нет
            "passport_date_of_birth": (str, Cdek._max_len_(10)),    # -- Дата рождения    date(yyyy - MM - dd)    нет
            "email": (str, Cdek._str_255_()),                       # -- Email --
            "phones": (list, None),                                 # -- Телефоны --
            "number": (str, Cdek._str_255_()),
        }, **kwargs)

    @staticmethod
    def order(**kwargs):
        return Cdek._construct_arg_({
            "order_uuid": (str, Cdek._uuid_()),
            "cdek_number": (int, None),
        }, **kwargs)

    def cities(self, country_codes: str = "RU", **kwargs):
        return self._get("location/cities", country_codes=country_codes, **kwargs)

    def regions(self, country_codes: str = "RU", **kwargs):
        return self._get("location/regions", country_codes=country_codes, **kwargs)

    def points(self, **kwargs):
        return self._get("deliverypoints", **kwargs)

    def tariff(self,
               tariff_code,         # -- Код тарифа, integer --
               from_location,       # -- Адрес отправления, location --
               to_location,         # -- Адрес получения, location --
               packages,            # -- Список информации по местам (упаковкам), package[] --
               services,            # -- Дополнительные услуги, service[] --
               **kwargs):
        return self._post_json("calculator/tariff", tariff_code=tariff_code, from_location=from_location, to_location=to_location, packages=packages, services=services, **kwargs)

    def tariff_list(self,
                    from_location,  # -- Адрес отправления, location --
                    to_location,    # -- Адрес получения, location --
                    packages,       # -- Список информации по местам (упаковкам), package[] --
                    **kwargs):
        return self._post_json("calculator/tarifflist", from_location=from_location, to_location=to_location, packages=packages, **kwargs)

    def delivery_cost(self, dst_city_code, weight, **kwargs):
        price = Decimal(str(kwargs['price']))
        tariff_code = int(self.setting("tariff_code"))
        src_city_code = int(self.setting("location_from_code"))
        try:
            tariff = self.tariff(
                tariff_code,
                Cdek.location(code=src_city_code),
                Cdek.location(code=dst_city_code),
                [Cdek.package(weight=weight)],
                [])
            return (d6y_cost_with_surcharges(self, Decimal(tariff["delivery_sum"]), price), tariff["period_min"], None) if "delivery_sum" in tariff and "period_min" in tariff else (None, None, Cdek.extract_error(tariff))
        except (KeyError, ValueError, TransportError):
            return None, None, "Не удалось определить параметры доставки"

    @staticmethod
    def _create_packages_by_order(r: Order):
        return [Cdek.package(
                number=str(r.uuid)[:23],
                weight=r.total_weight,
                length=r.length,
                width=r.width,
                height=r.height,
                comment=f"Заказ {r.uuid}",
                items=[Cdek.item(
                    name=i.product.title,
                    ware_key=i.ppk[:50],
                    payment=Cdek.money(value=0.0),
                    weight=i.weight,
                    cost=float(i.price.amount),
                    amount=i.quantity) for i in r.items.all()])]

    def _order_as_json(self, r: Order):
        opt = lambda **kwargs: {k: v for k, v in kwargs.items() if v is not None}
        return {
            "type": 1,
            "number": str(r.uuid),
            "tariff_code": int(self.setting("tariff_code")),
            "comment": str(r.uuid),
            "recipient": Cdek.recipient(name=r.cu_fullname, phones=[Cdek.phone(number=r.cu_phone)], **opt(email=r.cu_email)),
            "from_location": Cdek.location(code=int(self.setting("location_from_code")), address=Parameter.value_of("value_return_address_cd")),
            "to_location": Cdek.location(country_code="RU", code=r.city.code, address=r.delivery_address_for_cdek),
            "packages": self._create_packages_by_order(r),
            "print": "waybill",
        } | opt(delivery_recipient_cost=Cdek.money(value=float(r.delivery_cost.amount)) if settings.PREFERENCES.CoD(self.key) else None)

    @sleep_after()
    @on_exception_sleep_and_retry(1, (None, "Не удалось создать заказ на доставку"))
    def create_delivery_order(self, r: Order):
        jsn = self._order_as_json(r)
        if not jsn:
            raise ValueError(jsn)
        log_tg("Запрос на создание заказа на доставку:", jsn)
        result = self._post_json("orders", _json_=jsn)
        log_tg("Результат:", result)
        if 'entity' not in result or 'uuid' not in result['entity']:
            log_tg("Запрос провален")
            raise ValueError(result)
        log_tg("Запрос успешен")
        return result, None

    @sleep_after()
    @on_exception_sleep_and_retry(1, (None, "Не удалось создать документы к заказу на доставку"))
    def create_delivery_supplements(self, r):
        log_tg("Запрос на создание транспортных документов для:", r['entity']['uuid'])
        result = self._post_json(f'print/{self.stickers_type}', orders=[Cdek.order(order_uuid=r['entity']['uuid'])], copy_count=2)
        log_tg("Результат:", result)
        if 'entity' not in result or 'uuid' not in result['entity']:
            log_tg("Запрос провален")
            raise ValueError(result)
        log_tg("Запрос успешен")
        return result, None

    @sleep_after()
    @on_exception_sleep_and_retry(1, (None, "Не удалось загрузить документы к заказу на доставку"))
    def get_delivery_supplements_file(self, _, r):
        @sleep_after()
        def wait():
            return None
        log_tg("Запрос на URL транспортных документов:", f"""print/{self.stickers_type}/{r['entity']['uuid']}""")
        result = self._get(f"""print/{self.stickers_type}/{r['entity']['uuid']}""")
        log_tg("Результат:", result)
        if 'entity' not in result or 'url' not in result['entity']:
            log_tg("Запрос провален")
            raise ValueError(result)
        log_tg("Запрос успешен")
        wait()
        log_tg("Запрос на закачку транспортных документов:", result['entity']['url'])
        result = self._get_file(result['entity']['url'])
        log_tg("Результат:", result)
        if not result.is_success:
            log_tg("Запрос провален")
            raise ValueError(result.is_success)
        log_tg("Запрос успешен")
        return result.content, None

    @staticmethod
    def validate_destination(arg):
        match arg:
            case {
                "street": street,
                "building": building,
                "delivery_point": d6y_point
            } if (street is not None or settings.PREFERENCES.StreetCanBeMissed) and building is not None and d6y_point is None: return True
            case _: return False

