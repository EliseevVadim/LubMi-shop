import uuid

from django.utils.safestring import mark_safe
from customerinfo.customerinfo import CustomerInfo
from lms.coworkers.yookassa import Yookassa
from lms.forms import ShortCustomerInfoForm
from lms.models import Parameter


def parameters_processor(_):  # TODO -- dont forget fixtures for params! --
    return {
        f'param_{p.key}': mark_safe(p.value) for p in Parameter.objects.filter(in_context=True)
    }


def payment_processor(request):
    info = CustomerInfo(request)
    payment_id = info.payment_id
    if payment_id:
        yo = Yookassa()
        status = yo.get_payment_status(payment_id)
        try:
            if status in Yookassa.final_statuses:
                yo.payment_status_determined(payment_id, status)
            return {
                "payment_id": payment_id,
                "payment_status": status.value,
            } if status in Yookassa.notification_statuses else {}
        finally:
            if status not in Yookassa.transient_statuses:
                del info.payment_id
    return {}


def scui_processor(_):
    return {
        'scui_form': ShortCustomerInfoForm()
    }
