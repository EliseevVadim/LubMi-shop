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
        'w_heart': mark_safe("""<svg viewBox="-1 -1 26.56 23.000086"><path d="m 17.323638,1.0252719 c -2.1183,0 -3.9602,0.954402 -5.0436,2.553822 -1.0834,-1.59942 -2.9253399,-2.553822 -5.0436799,-2.553822 -1.60462,0.00187 -3.14299,0.639552 -4.27763,1.773162 -1.134636,1.13362 -1.772897,2.67059 -1.774766,4.27376 0,2.9428401 1.835896,6.0056201 5.457246,9.1016201 1.65941,1.4127 3.4518899,2.6616 5.3523299,3.729 0.0881,0.0472 0.1865,0.072 0.2865,0.072 0.1,0 0.1984,-0.0248 0.2865,-0.072 1.9004,-1.0674 3.6929,-2.3163 5.3523,-3.729 3.6213,-3.096 5.4572,-6.15878 5.4572,-9.1016201 -0.0018,-1.60317 -0.6401,-3.14014 -1.7747,-4.27376 -1.1347,-1.13361 -2.673,-1.771295 -4.2777,-1.773162 z"/></svg>"""),
        'left_arrow': mark_safe(f"""<img class="hand" src="{static("svg/larrow.svg")}"/>"""),
        'x_cross': mark_safe(f"""<img class="hand"  src="{static("svg/x-cross.svg")}"/>"""),
        'x_cross_nof': mark_safe(f"""<img class="hand"  src="{static("svg/x-cross-nof.svg")}"/>"""),
        'x_cross_ring': mark_safe(f"""<img class="hand"  src="{static("svg/x-cross-ring.svg")}"/>"""),
        'plus_ring': mark_safe(f"""<img class="hand"  src="{static("svg/plus-ring.svg")}"/>"""),
        'minus_ring': mark_safe(f"""<img class="hand"  src="{static("svg/minus-ring.svg")}"/>"""),
        'l_ang': mark_safe(f"""<img class="hand"  src="{static("svg/l-ang.svg")}"/>"""),
        'r_ang': mark_safe(f"""<img class="hand"  src="{static("svg/r-ang.svg")}"/>"""),
        'dl_ang': mark_safe(f"""<img class="hand"  src="{static("svg/dl-ang.svg")}"/>"""),
        'dr_ang': mark_safe(f"""<img class="hand"  src="{static("svg/dr-ang.svg")}"/>"""),
        'timer': mark_safe(f"""<img src="{static("svg/timer.svg")}"/>"""),
        'lens': mark_safe(f"""<img src="{static("svg/lens.svg")}"/>"""),
        'lens_gray': mark_safe(f"""<img src="{static("svg/lens-gray.svg")}"/>"""),
    }
