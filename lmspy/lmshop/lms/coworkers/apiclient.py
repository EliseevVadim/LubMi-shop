import httpx

from lms.models import Coworker
from urllib.parse import quote


class ApiClient:
    def __init__(self, key, address, client_id, client_secret):
        self._key = key
        self._address = address
        self._client_id = client_id
        self._client_secret = client_secret

    @staticmethod
    def _quoted(kwargs):
        return {quote(str(k)): quote(str(v)) for k, v in kwargs.items()}

    @property
    def key(self):
        return self._key

    @property
    def address(self):
        return self._address

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    def setting(self, name):
        return Coworker.setting(self.key, name)

    @property
    def authorization(self):
        return f"{self.client_id}:{self.client_secret}"

    def _post(self, func, **kwargs):
        with httpx.Client() as client:
            result = client.post(
                f"{self.address}/{func}",
                headers={
                    "Authorization": self.authorization,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data=ApiClient._quoted(kwargs)
            ).json()
            return result

    def _post_json(self, func, **kwargs):
        with httpx.Client() as client:
            result = client.post(
                f"{self.address}/{func}",
                headers={
                    "Authorization": self.authorization,
                    "Content-Type": "application/json"
                },
                json=kwargs
            ).json()
            return result

    def _get(self, func, **kwargs):
        with httpx.Client() as client:
            result = client.get(
                f"{self.address}/{func}",
                headers={
                    "Authorization": self.authorization,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                params=ApiClient._quoted(kwargs)
            ).json()
            return result
