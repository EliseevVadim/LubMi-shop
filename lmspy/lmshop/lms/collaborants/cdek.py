import httpx

from lms.models import Parameter
from urllib.parse import quote


class CDEK:
    def __init__(self,
                 address=Parameter.value_of("value_cdek_api_address"),
                 client_id=Parameter.value_of("value_cdek_client_id"),
                 client_secret=Parameter.value_of("value_cdek_client_secret")):
        self._address = address
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = None

    @property
    def auth(self):
        if self._token:
            return self._token
        with httpx.Client() as client:
            url = "http://localhost:8000/api/customer/checkout/"
            url = "https://api.edu.cdek.ru/v2/oauth/token"
            r = client.post(
                url,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "client_credentials",
                    "client_id": "EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI",
                    "client_secret": "PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG"
                }
            )
            _token = r.json()
            print(_token)
            return _token

    @auth.deleter
    def auth(self):
        self._token = None

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
    def client(self):
        client = httpx.Client()
        for h, v in {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }.items():
            client.headers[h] = v
        return client
