{% if payment_id %}
{% if payment_state != 'error' %}
{% if payment_state %}
setTimeout(() => {
    pmt_dialog.show('{% url "lms:message" kind="pmt" %}', () => { window.location.href='{{param_value_link_support}}'; })
}, 500);
//alert("Поздравляем с покупкой!"); // TODO custom message dialog call API to eliminate order // TODO webhooks!!!!!!!!!!!!
{% else %}
setTimeout(() => {
    nop_dialog.show('{% url "lms:message" kind="nop" %}', () => { window.location.href='{{param_value_link_support}}'; })
}, 500);
//alert("Жаль! Заказ отменен"); // TODO custom message dialog? call API to eliminate order
{% endif %}
{% else %}
setTimeout(() => {
    err_dialog.show('{% url "lms:message" kind="err" %}', () => { window.location.href='{{param_value_link_support}}'; })
}, 500);
//alert("При проверке статуса оплаты заказа произошла ошибка. Обновите страницу.");
{% endif %}
{% endif %}