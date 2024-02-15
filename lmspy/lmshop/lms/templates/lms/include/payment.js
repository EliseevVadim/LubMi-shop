{% if payment_id %}
const notifiers = {
    "succeeded": psu_dialog,
    "canceled": pca_dialog,
    "unknown": puk_dialog,
};
setTimeout(() => {notifiers['{{payment_status}}'].show('{% url "lms:payment_message" status=payment_status %}', () => { window.location.href='{{param_value_link_support}}'; })}, 500);
{% endif %}