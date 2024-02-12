from lms.coworkers.apiclient import ApiClient
from lms.models import Coworker, Order
from django.urls import reverse


class Yookassa(ApiClient):
    def __init__(self):
        super().__init__("yo", Coworker.setting("yo", "api_address"), Coworker.setting("yo", "account_id"), Coworker.setting("yo", "secret_key"))

    def create_payment(self, order: Order, summ):
        order_uuid = str(order.uuid)
        res = self._post_json(
            "payments",
            {"Idempotence-Key": order_uuid},
            (self.client_id, self.client_secret),
            amount={"value": f"{summ:.2f}", "currency": "RUB"},
            confirmation={"type": "redirect", "return_url": f'{self.setting("back_address")}{reverse("lms:about")}'},  # TODO !!
            capture=False,
            description=f"Заказ {order_uuid}",
            metadata={'orderNumber': order_uuid},
            receipt={
                "customer": {
                    "full_name": order.cu_fullname,
                    "email": order.cu_email,
                    "phone": order.cu_phone,
                },
                "items": [{
                    "description": item.title,
                    "quantity": f"{item.quantity}",
                    "amount": {
                        "value": f"{item.price.amount:.2f}",
                        "currency": "RUB"
                    },
                    "vat_code": self.setting("vat_code"),
                    "supplier": {
                        "name": self.setting("supplier_name"),
                        "phone": self.setting("supplier_phone"),
                        "inn": self.setting("supplier_inn")
                    }
                } for item in order.items.all()]
            })
        return res
