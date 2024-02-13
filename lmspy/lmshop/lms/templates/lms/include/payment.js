{% if payment_id %}
{% if payment_state != 'error' %}
{% if payment_state %}
alert("Поздравляем с покупкой!"); // TODO custom message dialog call API to eliminate order // TODO webhooks!!!!!!!!!!!!
{% else %}
alert("Жаль! Заказ отменен"); // TODO custom message dialog? call API to eliminate order
{% endif %}
{% else %}
alert("При проверке статуса оплаты заказа произошла ошибка. Обновите страницу.");
{% endif %}
{% endif %}