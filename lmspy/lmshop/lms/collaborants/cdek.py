import httpx

from lms.models import Parameter
from urllib.parse import quote
from datetime import datetime


class Cdek:
    def __init__(self,
                 address=Parameter.value_of("value_cdek_api_address"),
                 client_id=Parameter.value_of("value_cdek_client_id"),
                 client_secret=Parameter.value_of("value_cdek_client_secret")):
        self._address = address
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth = None
        self._tp_auth = None

    @staticmethod
    def _quoted(kwargs):
        return {quote(str(k)): quote(str(v)) for k, v in kwargs.items()}

    @property
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

        return self._auth if auth_alive() else ask_auth()

    @auth.deleter
    def auth(self):
        self._auth = None

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

    def post(self, func, **kwargs):
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

    def get(self, func, **kwargs):
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

    @property
    def cities(self):
        return self.get("location/cities")

    @property
    def regions(self):
        return self.get("location/regions")

    @property
    def points(self):
        return self.get("deliverypoints")
