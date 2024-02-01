c6t_dialog.form_container = () => document.querySelector("#c6t-dialog .c6t-form-container");
c6t_dialog.sidebar = () => document.querySelector("#c6t-dialog .c6t-sidebar");
c6t_dialog.__on_scart_changed = null;
const __close = c6t_dialog.close
c6t_dialog.close = () => {
    if(!!c6t_dialog.__on_scart_changed) {
        window.removeEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
        c6t_dialog.__on_scart_changed = null;
    }
    __close();
};
c6t_dialog.show = () => {
    fetch('{% url "lms:c6t_form" %}').then(response => response.text()).then(html => {
        c6t_dialog.close();
        c6t_dialog.body().innerHTML = '<div class="grid-c2"><div class="c6t-form-container"></div><div class="c6t-sidebar"></div></div>';
        c6t_dialog.form_container().innerHTML = html;
        c6t_dialog.__on_scart_changed = e => fetch('{% url "lms:c6t_scart" %}').then(response => response.text()).then(html => {
            c6t_dialog.sidebar().innerHTML = html;
        });
        window.addEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
        __api_call__('{% url "api:get_customer_info" flags=15 %}', null, answer => {
            let find = id => document.getElementById(id);

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
            _fullname.value = answer.address.fullname;

            _email.oninput = _ => { if(_email.value) _phone.removeAttribute('required'); else _phone.setAttribute('required',''); }
            _phone.oninput = _ => { if(_phone.value) _email.removeAttribute('required'); else _email.setAttribute('required',''); }

            _form.onsubmit = e => {
                e.preventDefault();
                __api_call__('{% url "api:c6t" %}', {
                    cu_name: _name.value,
                    cu_phone: _phone.value,
                    cu_email: _email.value
                }, result => {
                    if(result.success) {
                    } else {
                    }
                });
            }
            _email.oninput(null);
            _phone.oninput(null);

            c6t_dialog.self().showModal();
            scart_changed();
        });
    });
};
