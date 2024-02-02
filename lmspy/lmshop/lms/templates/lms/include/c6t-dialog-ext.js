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
    const by_id = id => document.getElementById(id);
    const by_selector = sel => document.querySelector(sel);
    fetch('{% url "lms:c6t_form" %}').then(response => response.text()).then(html => {
        c6t_dialog.close();
        c6t_dialog.body().innerHTML = `<div class="grid-c2">
    <section class="c6t-form-container">
    </section>
    <div class="items-top-down">
        <section class="c6t-sidebar">
        </section>
        <section id="c6t-status">
        </section>
    </div>
</div>
<section style="display:none" id="c6t-cl-holder">
</section>`;
        c6t_dialog.form_container().innerHTML = html;

        __api_call__('{% url "api:get_customer_info" flags=15 %}', null, answer => {
            _form = by_id('c6t-form');
            _name = by_id('c6t-cu_name');
            _phone = by_id('c6t-cu_phone');
            _email = by_id('c6t-cu_email');
            _city = by_id('c6t-cu_city');
            _street = by_id('c6t-cu_street');
            _building = by_id('c6t-cu_building');
            _entrance = by_id('c6t-cu_entrance');
            _floor = by_id('c6t-cu_floor');
            _apartment = by_id('c6t-cu_apartment');
            _fullname = by_id('c6t-cu_fullname');
            _confirm = by_id('c6t-cu_confirm');
            _d6y_service_0 = by_id('c6t-d6y_service_0');
            _d6y_service_1 = by_id('c6t-d6y_service_1');

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

            _email.oninput = _ => { 
                if(_email.value) _phone.removeAttribute('required'); 
                else _phone.setAttribute('required',''); 
            }
            
            _phone.oninput = _ => { 
                if(_phone.value) _email.removeAttribute('required'); 
                else _email.setAttribute('required',''); 
            }

            const update_summary = () => {
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                let url = '{% url "lms:c6t_info" kind="summary" data="dvservice" %}'.replace(/\/dvservice\/$/, `/${ds}/?city=${_city.value}`);
                fetch(url).then(response => response.text()).then(html => {
                    let c6t_status = by_id("c6t-status");
                    c6t_status.innerHTML = html;
                });
            };

            const d6y_changed = e => {
                let url = '{% url "lms:c6t_info" kind="cities" data="dvservice" %}'.replace(/\/dvservice\/$/, `/${e.currentTarget.value}/`);
                fetch(url).then(response => response.text()).then(html => {
                    dl_holder = by_id('c6t-cl-holder');
                    dl_holder.innerHTML = html;
                    _city.setAttribute('list', 'c6t-city-list');
                });
                update_summary();
            };

            _d6y_service_0.onchange = d6y_changed;
            _d6y_service_1.onchange = d6y_changed;
            _city.onchange = update_summary;

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
            c6t_dialog.__on_scart_changed = e => fetch('{% url "lms:c6t_scart" %}').then(response => response.text()).then(html => {
                c6t_dialog.sidebar().innerHTML = html;
                update_summary();
            });
            window.addEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
            fetch('{% url "lms:c6t_info" kind="delivery" data="sd" %}').then(response => response.text()).then(html => {
                _d6y_service_0.parentElement.insertAdjacentHTML('beforeEnd', html);
            });
            fetch('{% url "lms:c6t_info" kind="delivery" data="pr" %}').then(response => response.text()).then(html => {
                _d6y_service_1.parentElement.insertAdjacentHTML('beforeEnd', html);
            });

            scart_changed();
            d6y_changed({currentTarget: by_selector('input[id^="c6t-d6y_service_"]:checked')});
            _email.oninput(null);
            _phone.oninput(null);

            c6t_dialog.self().showModal();
        });
    });
};
