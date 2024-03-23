from httpx import TransportError
from lms.coworkers.apiclient import ApiClient
from lms.coworkers.dadata import DaData
from lms.models import Coworker, City
from lms.utils import D6Y


class PostRu(ApiClient):
    acceptable_quality_codes = frozenset({'GOOD', 'POSTAL_BOX', 'ON_DEMAND', 'UNDEF_05'})
    acceptable_validation_codes = frozenset({'VALIDATED', 'OVERRIDDEN' 'CONFIRMED_MANUALLY'})

    def __init__(self):
        super().__init__(D6Y.PR, Coworker.setting(D6Y.PR, "api_address"), "", "")
        self._access_token = self.setting("access_token")
        self._user_auth_key = self.setting("user_auth_key")

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
        dadata = DaData()
        try:
            suggestions = dadata.pru_points(DaData.location(lat=float(city.latitude), lon=float(city.longitude), radius_meters=float(5000)))['suggestions']
            postal_code = next((x['data']['postal_code'] for x in suggestions
                                if 'data' in x and 'postal_code' in x['data'] and 'is_closed' in x['data'] and 'type_code' in x['data'] and
                                   x['data']['type_code'].lower() not in ['почтомат', 'ти'] and not x['data']['is_closed']),
                               None)
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
