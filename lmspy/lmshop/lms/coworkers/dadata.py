from lms.coworkers.abstractapiclient import AbstractApiClient
from lms.models import Coworker


class DaData(AbstractApiClient):
    def __init__(self):
        super().__init__(
            self.setting("api_address"),
            None,
            self.setting("access_token"))

    @property
    def key(self):
        return 'dd'

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

    def pos_ru_points(self, location, **kwargs):
        return self._post_json("geolocate/postal_unit", **location, **kwargs)

    def suggest_address(self, **kwargs):
        return self._post_json("suggest/address", **kwargs)
