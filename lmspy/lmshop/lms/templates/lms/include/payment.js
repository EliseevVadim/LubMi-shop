{% if payment_id %}
__api_call__('{% url "api:set_payment_state" %}', { payment_id: '{{payment_id}}' }, result => {if(!result.success) {show_js_message(result.why);}});
{% if payment_state != 'error' %}
{% if payment_state %}
setTimeout(() => {pmt_dialog.show('{% url "lms:message" kind="pmt" %}', () => { window.location.href='{{param_value_link_support}}'; })}, 500);
{% else %}
setTimeout(() => {nop_dialog.show('{% url "lms:message" kind="nop" %}', () => { window.location.href='{{param_value_link_support}}'; })}, 500);
{% endif %}
{% else %}
setTimeout(() => {per_dialog.show('{% url "lms:message" kind="per" %}', () => { window.location.href='{{param_value_link_support}}'; })}, 500);
{% endif %}
{% endif %}