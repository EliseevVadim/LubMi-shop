c6t_dialog.form_container = () => document.querySelector("#c6t-dialog .c6t-form-container");
c6t_dialog.sidebar = () => document.querySelector("#c6t-dialog .c6t-sidebar");
c6t_dialog.city_list = () => document.querySelector("#c6t-dialog .c6t-city-list");
c6t_dialog.__on_scart_changed = null;
c6t_dialog.__close = c6t_dialog.close;
c6t_dialog.close = () => {
    if(!!c6t_dialog.__on_scart_changed) {
        window.removeEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
        c6t_dialog.__on_scart_changed = null;
    }
    c6t_dialog.rszo = null;
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
</div>`;
        c6t_dialog.form_container().innerHTML = html;

        __api_call__('{% url "api:get_customer_info" flags=15 %}', null, answer => {
            _form = by_id('c6t-form');
            _name = by_id('c6t-cu_name');
            _phone = by_id('c6t-cu_phone');
            _email = by_id('c6t-cu_email');
            _city_uuid = by_id('c6t-cu_city_uuid');
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
            _city_uuid.value = answer.address.city_uuid;
            _city.value = answer.address.city;
            _street.value = answer.address.street;
            _building.value = answer.address.building;
            _entrance.value = answer.address.entrance;
            _floor.value = answer.address.floor;
            _apartment.value = answer.address.apartment;
            _fullname.value = answer.address.fullname;

            const city_chosen = () => !!_city_uuid.value;
            c6t_dialog.choose_city = (text, uuid) => {
                _city_uuid.value = uuid;
                _city.value = text;
                c6t_dialog.city_list().style.visibility = 'hidden';
                setTimeout(update_summary);
            }

            _city.insertAdjacentHTML("afterEnd", '<div id="c6t-city-list" class="c6t-city-list"></div>');
            const move_city_list = elements => {
                cl = c6t_dialog.city_list();
                pe = _city.parentElement;
                cl.style.transform = `translate(0px, ${pe.clientHeight + 5}px)`;
                cl.style.width = `${_city.clientWidth}px`;
            }; setTimeout(move_city_list);

            const update_cities = () => {
                if(_city.controller) { _city.controller.abort(); }
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                let url = '{% url "lms:c6t_info" kind="cities" data="dvservice" %}'.replace(/\/dvservice\/$/, `/${ds}/?city=${_city.value}`);
                _city.controller = new AbortController();
                fetch(url, {signal: _city.controller.signal}).then(response => response.text()).then(html => {
                    _city.controller = null;
                    c6t_dialog.city_list().innerHTML = html;
                    c6t_dialog.city_list().style.visibility = 'visible';
                }).catch(_=>{});
            };

            const update_summary = () => {
                let c6t_status = by_id("c6t-status");
                if(c6t_status.controller) { c6t_status.controller.abort(); }
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                let url = '{% url "lms:c6t_info" kind="summary" data="dvservice" %}'.replace(/\/dvservice\/$/, `/${ds}/?city_uuid=${_city_uuid.value}`);
                c6t_status.controller = new AbortController();
                fetch(url, {signal: c6t_status.controller.signal}).then(response => response.text()).then(html => {
                    c6t_status.controller = null;
                    c6t_status.innerHTML = html;
                }).catch(_=>{});
            };

            const d6y_changed = () => {
                if(!city_chosen()) { setTimeout(update_cities); }
                setTimeout(update_summary);
            };

            _email.oninput = _ => { 
                if(_email.value) _phone.removeAttribute('required'); 
                else _phone.setAttribute('required',''); 
            }
            
            _phone.oninput = _ => { 
                if(_phone.value) _email.removeAttribute('required'); 
                else _email.setAttribute('required',''); 
            }

            _city.tmo_id = null;
            _city.oninput = e => {
                if(_city.tmo_id) { clearTimeout(_city.tmo_id); }
                if(city_chosen()) {
                    _city.value = null;
                    _city_uuid.value = null;
                    setTimeout(update_summary)
                }
                _city.tmo_id = setTimeout(() => {
                    update_cities();
                    _city.tmo_id = null;
                }, 1000);
            };

            _d6y_service_0.onchange = d6y_changed;
            _d6y_service_1.onchange = d6y_changed;

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
                        alert(result.why); //TODO custom message box
                    }
                });
            }

            c6t_dialog.__on_scart_changed = e => fetch('{% url "lms:c6t_scart" %}').then(response => response.text()).then(html => {
                c6t_dialog.sidebar().innerHTML = html;
                update_summary();
            });
            window.addEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
            fetch('{% url "lms:c6t_info" kind="delivery" data="cd" %}').then(response => response.text()).then(html => {
                _d6y_service_0.parentElement.insertAdjacentHTML('beforeEnd', html);
            });
            fetch('{% url "lms:c6t_info" kind="delivery" data="pr" %}').then(response => response.text()).then(html => {
                _d6y_service_1.parentElement.insertAdjacentHTML('beforeEnd', html);
            });

            scart_changed();
            d6y_changed({currentTarget: by_selector('input[id^="c6t-d6y_service_"]:checked')});
            _email.oninput(null);
            _phone.oninput(null);
            c6t_dialog.rszo = new ResizeObserver(move_city_list);
            c6t_dialog.rszo.observe(_city);
            c6t_dialog.self().showModal();
        });
    });
};
