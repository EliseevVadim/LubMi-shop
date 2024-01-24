import json
import httpx
from threading import Thread


class Telegram:
    def __init__(self, token: str, cids: frozenset[int]):
        self._token = token
        self._cids = cids

    def send_message(self, message: str):
        def send_msg(token, cid, text):
            with httpx.Client() as client:
                try:
                    client.headers["Content-Type"] = "application/json"
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    content = json.dumps({'chat_id': cid, 'text': text})
                    res = client.post(url, content=content)
                    if res.is_error:
                        print(res.text)
                except httpx.TransportError as e:
                    print(e)
                    pass

        for _cid in self._cids:
            th = Thread(target=send_msg, args=(self._token, _cid, message), daemon=True)
            th.start()
