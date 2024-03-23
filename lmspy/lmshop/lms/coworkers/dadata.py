from lms.coworkers.apiclient import ApiClient
from lms.models import Coworker


class DaData(ApiClient):
    def __init__(self):
        super().__init__("dd", Coworker.setting("dd", "api_address"), None, Coworker.setting("dd", "access_token"))

    @property
    def authorization(self):
        return f"{self.token_type} {self.access_token}"

    @property
    def basic_auth(self):
        return None

    @property
    def access_token(self):
        return self.client_secret

    @property
    def token_type(self):
        return "Token"

    @staticmethod
    def location(**kwargs):
        return DaData._construct_arg_({
            "lon": (float, None),                               # -- Долгота, float
            "lat": (float, None),                               # -- Широта, float
            "radius_meters": (float, DaData._positive_()),      # -- Радиус
        }, **kwargs)

    def pru_points(self, location, **kwargs):
        return self._post_json("geolocate/postal_unit", **location, **kwargs)
