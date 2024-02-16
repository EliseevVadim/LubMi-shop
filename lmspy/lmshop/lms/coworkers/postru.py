from httpx import TransportError

from lms.coworkers.apiclient import ApiClient
from lms.models import Coworker


class PostRu(ApiClient):
    q_codes = frozenset({'GOOD', 'POSTAL_BOX', 'ON_DEMAND', 'UNDEF_05'})
    v_codes = frozenset({'VALIDATED', 'OVERRIDDEN' 'CONFIRMED_MANUALLY'})

    def __init__(self):
        super().__init__("pr", Coworker.setting("pr", "api_address"), "", "")
        self._token = self.setting("access_token")
        self._user_key = self.setting("user_auth_key")

    @property
    def token(self):
        return self._token

    @property
    def user_key(self):
        return self._user_key

    @property
    def authorization(self):
        return f"AccessToken {self.token}"

    @property
    def basic_auth(self):
        return None

    def compose_headers(self, content_type, headers):
        xua = {"X-User-Authorization": f"Basic {self.user_key}"} if self.user_key else {}
        ctp = {"Content-type": "application/json;charset=UTF-8"}
        a = {"Accept": "application/json;charset=UTF-8"}
        return super().compose_headers(content_type, headers) | xua | ctp | a

    def index_by_address(self, address):
        na = self._post_json("clean/address", _json_=[{
            "id": "1",
            "original-address": address,
        }])[0]
        if not (na["quality-code"] in PostRu.q_codes and na["validation-code"] in PostRu.v_codes):
            raise ValueError(na)
        return na["index"]

    def tariff(self, index, price, weight):
        tf = self._post_json(
            "tariff",
            _json_={
                "index-to": index,
                "declared-value": price,
                "mail-category": "WITH_DECLARED_VALUE",
                "mail-type": "PARCEL_CLASS_1",
                "mass": weight,
                "notice-payment-method": "CASHLESS",
                "payment-method": "CASHLESS",
                "sms-notice-recipient": 0,
                "transport-type": "SURFACE",
                "with-order-of-notice": False,
                "with-simple-notice": False
            })
        return tf

    def delivery_cost(self, _, weight, **kwargs):  # TODO implement
        city, street, building, price = str(kwargs['city']), str(kwargs['street']), str(kwargs['building']), str(kwargs['price'])
        price = int(round(float(price) * 100))
        try:
            index = self.index_by_address(','.join([city, street, building]))
        except (KeyError, ValueError, TransportError):
            return None, None, "Не удалось подтвердить адрес доставки"
        tariff = {}
        try:
            tariff = self.tariff(index, price, weight)
            return tariff["total-rate"] / 100.0, tariff["delivery-time"]["min-days"], None
        except (KeyError, ValueError, TransportError):
            return None, None, tariff['desc'] if 'desc' in tariff else "Не удалось определить параметры доставки"
