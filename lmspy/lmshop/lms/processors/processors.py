from django.utils.safestring import mark_safe
from customerinfo.customerinfo import CustomerInfo
from lms.coworkers.yookassa import Yookassa
from lms.forms import ShortCustomerInfoForm
from lms.models import Parameter


def parameters_processor(_):  # TODO -- dont forget fixtures for params! --
    return {
        f'param_{p.key}': mark_safe(p.value) for p in Parameter.objects.filter(in_context=True)
    }


def payment_processor(request):  # TODO -- dont forget WebHooks for payment checks! --
    info = CustomerInfo(request)
    payment_id = info.payment_id
    if payment_id:
        state, error = Yookassa().payment_state(payment_id)
        try:
            return {
                "payment_id": payment_id,
                "payment_state": "error",
                "payment_error": error
            } if error else {
                "payment_id": payment_id,
                "payment_state": state,
            }
        finally:
            if not error:
                del info.payment_id
    return {}


def scui_processor(_):
    return {
        'scui_form': ShortCustomerInfoForm()
    }
