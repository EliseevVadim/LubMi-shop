from httpx import TransportError

from lms.api.decorators import sleep_and_retry_on_except, sleep_after
from lms.coworkers.apiclient import ApiClient
from lms.coworkers.dadata import DaData
from lms.models import Coworker, City, Order
from lms.defines import D6Y


class PostRu(ApiClient):
    acceptable_quality_codes = frozenset({'GOOD', 'POSTAL_BOX', 'ON_DEMAND', 'UNDEF_05'})
    acceptable_validation_codes = frozenset({'VALIDATED', 'OVERRIDDEN' 'CONFIRMED_MANUALLY'})

    def __init__(self):
        super().__init__(D6Y.PR, Coworker.setting(D6Y.PR, "api_address"), "", "")
        self._access_token = self.setting("access_token")
        self._user_auth_key = self.setting("user_auth_key")

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
        price = str(kwargs['price'])
        price = int(round(float(price) * 100))
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

        tariff = {}
        try:
            tariff = self.tariff(postal_code, price, weight)
            delay = tariff["delivery-time"]["min-days"] if "min-days" in tariff["delivery-time"] else tariff["delivery-time"]["max-days"]
            return tariff["total-rate"] / 100.0, delay, None
        except (KeyError, ValueError, TransportError):
            return None, None, tariff['desc'] if 'desc' in tariff else "Не удалось определить параметры доставки"

    def index_by_address(self, address: str):
        result = self._post_json("clean/address", _json_=[{"id": "0", "original-address": address}])[0]
        return result["index"] if "index" in result else None

    def _order_as_json(self, r: Order, mail_type=None):
        """Can throw KeyError, ValueError, TransportError or return empty result"""
        index = self.index_by_address(r.delivery_address_short)
        return index and {
            # "add-to-mmo": True,
            # "address-from": {
            #     "address-type": "DEFAULT",
            #     "area": "string",
            #     "building": "string",
            #     "corpus": "string",
            #     "hotel": "string",
            #     "house": "string",
            #     "index": "string",
            #     "letter": "string",
            #     "location": "string",
            #     "num-address-type": "string",
            #     "office": "string",
            #     "place": "string",
            #     "region": "string",
            #     "room": "string",
            #     "slash": "string",
            #     "street": "string",
            #     "vladenie": "string"
            # },
            "address-type-to": "DEFAULT",
            # "area-to": "string",
            # "branch-name": "string",
            # "building-to": r.cu_building,
            "comment": f"Заказ {str(r.uuid)}",
            "completeness-checking": False,
            # "compulsory-payment": 0,
            # "corpus-to": "string",
            "courier": False,
            # "customs-declaration": {
            #     "certificate-number": "string",
            #     "currency": "string",
            #     "customs-code": "string",
            #     "ioss-code": "string",
            #     "customs-entries": [
            #         {
            #             "amount": 0,
            #             "country-code": 0,
            #             "description": "string",
            #             "tnved-code": "string",
            #             "trademark": "string",
            #             "value": 0,
            #             "weight": 0
            #         }
            #     ],
            #     "entries-type": "GIFT",
            #     "invoice-number": "string",
            #     "license-number": "string",
            #     "with-certificate": True,
            #     "with-invoice": True,
            #     "with-license": True
            # },
            "delivery-to-door": False,
            "delivery-with-cod": False,
            # "dimension": {
            #     "height": 0,
            #     "length": 0,
            #     "width": 0
            # },
            # "dimension-type": "S",
            # "easy-return": True,
            # "ecom-data": {
            #     "delivery-point-index": "string",
            #     "identity-methods": [
            #         "WITHOUT_IDENTIFICATION"
            #     ],
            #     "services": [
            #         "WITHOUT_SERVICE"
            #     ]
            # },
            # "farma": True,
            # "envelope-type": "C4",
            # "fiscal-data": {
            #     "customer-email": "string",
            #     "customer-inn": "string",
            #     "customer-name": "string",
            #     "customer-phone": 0,
            #     "payment-amount": 0
            # },
            "fragile": False,
            "given-name": r.cu_fullname,
            # "goods": {
            #     "items": [
            #         {
            #             # "code": "string",
            #             # "country-code": 0,
            #             # "customs-declaration-number": "string",
            #             "description": i.product.title,
            #             # "excise": 0,
            #             "goods-type": "GOODS",
            #             "insr-value": int(i.price.amount * 100),
            #             "item-number": i.product.article,
            #             # "lineattr": 0,
            #             # "payattr": 0,
            #             "quantity": i.quantity,
            #             # "supplier-inn": "string",
            #             # "supplier-name": "string",
            #             # "supplier-phone": "string",
            #             "value": int(i.price.amount * 100),
            #             # "vat-rate": 0,
            #             "weight": i.weight,
            #         }
            #         for i in r.items.all()]
            # },
            # "group-name": "string",
            # "hotel-to": "string",
            "house-to": r.cu_building,
            "index-to": int(index),
            # "inner-num": "string",
            "insr-value": int(r.total_price.amount * 100),
            # "inventory": True,
            # "letter-to": "string",
            # "location-to": "string",
            # "manual-address-input": True,
            "mail-category": self.setting("mail_category"),
            "mail-direct": 643,
            "mail-type": mail_type if mail_type is not None else self.setting("mail_type"),
            "mass": r.total_weight,
            # "middle-name": "string",
            # "no-return": True,
            # "notice-payment-method": "CASHLESS",
            # "num-address-type-to": "string",
            # "office-to": "string",
            "order-num": str(r.uuid),
            # "payment": 0,
            # "payment-method": "CASHLESS",
            "place-to": r.city.city,
            "postoffice-code": self.setting("postoffice-code", "350020"),
            # "pre-postal-preparation": True,
            # "prepaid-amount": 0,
            "recipient-name": r.cu_fullname,
            "region-to": r.cu_city_region,
            # "room-to": "string",
            # "sender-comment": "string",
            # "sender-name": "string",
            # "shelf-life-days": 0,
            # "slash-to": "string",
            # "sms-notice-recipient": 0,
            # "str-index-to": "",
            "street-to": r.cu_street,
            "surname": r.cu_last_name,
            # "tel-address": 79180082891,
            # "tel-address-from": 0,
            # "time-slot-id": 0,
            # "transport-mode": "STANDARD",
            # "transport-type": "SURFACE",
            # "vladenie-to": "string",
            # "vsd": True,
            # "with-documents": True,
            # "with-electronic-notice": True,
            # "with-goods": True,
            # "with-order-of-notice": True,
            # "with-packaging": True,
            # "with-simple-notice": True,
            # "wo-mail-rank": True
        }

    @sleep_after()
    @sleep_and_retry_on_except(1, (None, "Не удалось создать заказ на доставку"))
    def create_delivery_order(self, r: Order):
        jsn = self._order_as_json(r)
        if not jsn:
            raise ValueError(jsn)
        result = self._put_json("user/backlog", _json_=[jsn])
        if "result-ids" not in result or not result["result-ids"]:
            raise ValueError(result)
        return result, None

    @sleep_after()
    @sleep_and_retry_on_except(1, (None, "Не удалось создать документы к заказу на доставку"))
    def create_delivery_supplements(self, r):
        @sleep_after()
        def wait():
            return None
        result = self._post_json("user/shipment", _json_=[r["result-ids"][0]])
        if "result-ids" not in result or not result["result-ids"]:
            raise ValueError(result)
        wait()
        self._post_json(f"batch/{result['batches'][0]['batch-name']}/checkin")
        return result, None

    @sleep_after()
    @sleep_and_retry_on_except(1, (None, "Не удалось загрузить документы к заказу на доставку"))
    def get_delivery_supplements_file(self, r, _):
        url = self.func_url(f"forms/{r["result-ids"][0]}/f7pdf")
        result = self._get_file(url)
        if not result.is_success:
            raise ValueError(result.is_success)
        return result.content, None
