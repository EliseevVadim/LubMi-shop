from django.templatetags.static import static
from django.utils.safestring import mark_safe
from customerinfo.customerinfo import CustomerInfo
from lms.api.business import check_payment_life_cycle_is_completed
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
        payment_status, payment = yo.get_payment_status(payment_id)
        try:
            check_payment_life_cycle_is_completed(payment_id, payment_status, payment)
            return {
                "payment_id": payment_id,
                "payment_status": payment_status.value,
            } if payment_status in Yookassa.payment_statuses_are_notification_subjects else {}
        finally:
            if payment_status not in Yookassa.transient_payment_statuses:
                del info.payment_id
    return {}


def scui_processor(_):
    return {
        'scui_form': ShortCustomerInfoForm()
    }


def shorts_processor(_):
    return {
        'separator': mark_safe("""<div class="separator"><svg class="separator" viewBox="0 0 10 5" preserveAspectRatio="none"><line x1="0" y1="0" x2="10" y2="0"/><line x1="5" y1="0" x2="5" y2="5"/></svg></div>"""),
        'left_arrow': mark_safe(f"""<img class="hand" src="{static("svg/larrow.svg")}"/>"""),
        'x_cross': mark_safe(f"""<img class="hand"  src="{static("svg/x-cross.svg")}"/>"""),
        'timer': mark_safe(f"""<img src="{static("svg/timer.svg")}"/>"""),
        'lens': mark_safe(f"""<img src="{static("svg/lens.svg")}"/>"""),
    }
