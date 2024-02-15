import httpx
import functools
import re

from lms.models import Coworker
from urllib.parse import quote


class ApiClient:
    def __init__(self, key, address, client_id, client_secret):
        self._key = key
        self._address = address
        self._client_id = client_id
        self._client_secret = client_secret

    uuid_re = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$")

    @staticmethod
    def _quoted(kwargs):
        return {quote(str(k)): quote(str(v)) for k, v in kwargs.items()}

    def _compose_headers(self, content_type, headers):
        auth_str = self.authorization
        return {"Content-Type": content_type} | ({"Authorization": auth_str} if auth_str else {}) | ({h: v for h, v in headers.items()} if headers else {})

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
        return None

    def func_url(self, func):
        return f"{self.address}/{func}"

    def _post_x_www_form(self, func, headers=None, auth=None, **kwargs):
        with httpx.Client() as client:
            result = client.post(
                self.func_url(func),
                auth=auth,
                headers=self._compose_headers("application/x-www-form-urlencoded", headers),
                data=ApiClient._quoted(kwargs)
            ).json()
            return result

    def _post_json(self, func, headers=None, auth=None, **kwargs):
        with httpx.Client() as client:
            result = client.post(
                self.func_url(func),
                auth=auth,
                headers=self._compose_headers("application/json", headers),
                json=kwargs
            ).json()
            return result

    def _get(self, func, headers=None, auth=None, **kwargs):
        with httpx.Client() as client:
            result = client.get(
                self.func_url(func),
                auth=auth,
                headers=self._compose_headers("application/x-www-form-urlencoded", headers),
                params=ApiClient._quoted(kwargs)
            ).json()
            return result

    @staticmethod
    # @functools.lru_cache
    def _construct_arg_(decl: dict[str, tuple], **kwargs):
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
        return ApiClient._max_len_(2)

    @staticmethod
    @functools.lru_cache
    def _str_255_():
        return ApiClient._max_len_(255)

    @staticmethod
    @functools.lru_cache
    def _uuid_():
        return lambda v: bool(ApiClient.uuid_re.match(v))

    @staticmethod
    @functools.lru_cache
    def _one_of_(*args):
        return lambda v: v in frozenset(args)

