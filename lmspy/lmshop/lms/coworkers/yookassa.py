from lms.coworkers.apiclient import ApiClient
from lms.deco import copy_result
from lms.models import Coworker
from urllib.parse import quote
from django.core.cache import cache


class Yookassa(ApiClient):
    def __init__(self):
        super().__init__("yo", Coworker.setting("yo", "api_address"), Coworker.setting("yo", "account_id"), Coworker.setting("cd", "client_secret"))
