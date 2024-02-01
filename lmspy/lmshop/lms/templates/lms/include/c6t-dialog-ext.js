c6t_dialog.form_container = () => document.querySelector("#c6t-dialog .c6t-form-container");
c6t_dialog.sidebar = () => document.querySelector("#c6t-dialog .c6t-sidebar");
c6t_dialog.__on_scart_changed = null;
c6t_dialog.__close = c6t_dialog.close;
c6t_dialog.close = () => {
    if(!!c6t_dialog.__on_scart_changed) {
        window.removeEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
        c6t_dialog.__on_scart_changed = null;
    }
    c6t_dialog.__close();
};
c6t_dialog.show = () => {
    const find = id => document.getElementById(id);
    fetch('{% url "lms:c6t_form" %}').then(response => response.text()).then(html => {
        c6t_dialog.close();
        c6t_dialog.body().innerHTML = '<div class="grid-c2"><div class="c6t-form-container"></div><div class="items-top-down"><div class="c6t-sidebar"></div><h5 id="c6t-status">Проверка</h5></div></div>';
        c6t_dialog.form_container().innerHTML = html;

        __api_call__('{% url "api:get_customer_info" flags=15 %}', null, answer => {
            _form = find('c6t-form');
            _name = find('c6t-cu_name');
            _phone = find('c6t-cu_phone');
            _email = find('c6t-cu_email');
            _city = find('c6t-cu_city');
            _street = find('c6t-cu_street');
            _building = find('c6t-cu_building');
            _entrance = find('c6t-cu_entrance');
            _floor = find('c6t-cu_floor');
            _apartment = find('c6t-cu_apartment');
            _fullname = find('c6t-cu_fullname');
            _confirm = find('c6t-cu_confirm');
            _d7y_service_0 = find('c6t-d7y_service_0');
            _d7y_service_1 = find('c6t-d7y_service_1');

            _name.value = answer.name;
            _phone.value = answer.phone;
            _email.value = answer.email;
            _city.value = answer.address.city;
            _street.value = answer.address.street;
            _building.value = answer.address.building;
            _entrance.value = answer.address.entrance;
            _floor.value = answer.address.floor;
            _apartment.value = answer.address.apartment;
            _fullname.value = answer.address.fullname; // TODO -- ask services for data!! --
            _d7y_service_0.parentElement.insertAdjacentHTML('beforeEnd', "<span class='gray'> от 3 дней, от 459 руб.</span>");
            _d7y_service_1.parentElement.insertAdjacentHTML('beforeEnd', "<span class='gray'> от 3 дней, от 459 руб.</span>");

            _email.oninput = _ => { if(_email.value) _phone.removeAttribute('required'); else _phone.setAttribute('required',''); }
            _phone.oninput = _ => { if(_phone.value) _email.removeAttribute('required'); else _email.setAttribute('required',''); }

            let calculate_summary = () => __api_call__('{% url "api:scart_state" %}', null, answer => {
                let c6t_status = find("c6t-status");
                if(answer.success) {
                    stat_str = answer.record_count > 0 ? "Сумма: " + answer.price + "руб.<br/>Доставка: 719 руб.<br/>Россия, г.Москва<br/>Итоговая сумма: " + (answer.price + 719) + "руб." : "Нет товаров в заказе";
                    c6t_status.innerHTML = stat_str;
                } else {
                    alert("Ошибка сервера. Оформление заказа будет прервано!");
                    c6t_dialog.close();
                }
            });

            _form.onsubmit = e => {
                e.preventDefault();
                __api_call__('{% url "api:c6t" %}', {
                    cu_name: _name.value,
                    cu_phone: _phone.value,
                    cu_email: _email.value
                    // TODO -- other --
                }, result => {
                    if(result.success) {
                    } else {
                        alert(result.why);
                    }
                });
            }
            _email.oninput(null);
            _phone.oninput(null);

            c6t_dialog.__on_scart_changed = e => fetch('{% url "lms:c6t_scart" %}').then(response => response.text()).then(html => {
                c6t_dialog.sidebar().innerHTML = html;
                calculate_summary();
            });
            window.addEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
            c6t_dialog.self().showModal();
            scart_changed();
        });
    });
};
