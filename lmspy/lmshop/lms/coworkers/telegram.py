import json
from threading import Thread
import httpx


class Telegram:
    def __init__(self, token: str, cids: frozenset[int]):
        self._token = token
        self._cids = cids

    def send(self, message: str):
        def send_msg(token, cid, text):
            with httpx.Client() as client:
                try:
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    client.headers["Content-Type"] = "application/json"
                    res = client.post(url, json={'chat_id': cid, 'parse_mode': 'Markdown', 'text': text})
                    if res.is_error:
                        print(res.text)
                except httpx.TransportError as e:
                    print(e)
                    pass

        for _cid in self._cids:
            th = Thread(target=send_msg, args=(self._token, _cid, message), daemon=True)
            th.start()
