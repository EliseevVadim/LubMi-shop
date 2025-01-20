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
            "recipient": Cdek.recipient(name=r.cu_fullname, phones=[Cdek.phone(number=r.cu_phone)], **opt(email=r.cu_email)),
            "shipment_point": self.setting("shipment_point"),
            "delivery_point": r.delivery_point,
            "packages": self._create_packages_by_order(r),
            "print": "waybill",
        } | opt(delivery_recipient_cost=Cdek.money(value=float(r.delivery_cost.amount)) if settings.PREFERENCES.CoD(self.key) else None)

    @staticmethod
    def validate_destination(arg):
        match arg:
            case {"delivery_point": d6y_point, **wtf} if d6y_point is not None and set(wtf.values()) == {None}: return True
            case _: return False
