from lms.coworkers.cdek import Cdek
from lms.d6y import D6Y
from lms.models import Order, Parameter
from django.conf import settings


class CdekP(Cdek):
    @property
    def key(self):
        return D6Y.CP

    def _order_as_json(self, r: Order):
        opt = lambda **kwargs: {k: v for k, v in kwargs.items() if v is not None}
        return {
            "type": 1,
            "number": str(r.uuid),
            "tariff_code": int(self.setting("tariff_code")),
            "comment": str(r.uuid),
            "recipient": Cdek.recipient(
                name=r.cu_fullname,
                phones=[Cdek.phone(number=r.cu_phone)],
                **opt(email=r.cu_email)),
            "shipment_point": self.setting("shipment_point"),
            "delivery_point": r.delivery_point,
            "packages": [Cdek.package(
                number=str(r.uuid)[:23],
                weight=r.total_weight,
                length=r.length,
                width=r.width,
                height=r.height,
                comment=f"Заказ {r.uuid}",
                items=[Cdek.item(
                    name=i.product.title,
                    ware_key=i.ppk[:50],
                    payment=Cdek.money(value=0.0),
                    weight=i.weight,
                    cost=float(i.price.amount),
                    amount=i.quantity) for i in r.items.all()])],
            "print": "waybill",
        } | opt(delivery_recipient_cost=Cdek.money(value=float(r.delivery_cost.amount)) if settings.PREFERENCES.c_o_d(self.key) else None)

    @staticmethod
    def validate_destination(arg):
        match arg:
            case {"delivery_point": d6y_point, **wtf} if d6y_point is not None and set(wtf.values()) == {None}:
                return True
            case _:
                return False
