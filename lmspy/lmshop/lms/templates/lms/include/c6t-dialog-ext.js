c6t_dialog.form_container = () => document.querySelector("#c6t-dialog .c6t-form-container");
c6t_dialog.sidebar = () => document.querySelector("#c6t-dialog .c6t-sidebar");
c6t_dialog.city_list = () => document.querySelector("#c6t-dialog .c6t-city-list");
c6t_dialog.cd_info = () => document.querySelector("#c6t-dialog #c6t-cd-info");
c6t_dialog.pr_info = () => document.querySelector("#c6t-dialog #c6t-pr-info");
c6t_dialog.ready = () => document.querySelector("#c6t-dialog #c6t-d6y-ready");
c6t_dialog.button = () => document.querySelector("#c6t-dialog #c6t-submit-button");
c6t_dialog.iid = undefined;
c6t_dialog.__on_scart_changed = null;
c6t_dialog.__close = c6t_dialog.close;
c6t_dialog.close = () => {
    if(!!c6t_dialog.__on_scart_changed) {
        window.removeEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
        c6t_dialog.__on_scart_changed = null;
    }
    if(!!c6t_dialog.iid) {
        clearInterval(c6t_dialog.iid);
        c6t_dialog.iid = undefined;
    }
    c6t_dialog.rszo = null;
    c6t_dialog.__close();
};

class Dropdown {
    constructor(input, id, updater) {
        let move_dropdown = _ => {
            let dd = document.querySelector(`#${id}`);
            let pe = input.parentElement;
            dd.style.transform = `translate(0px, ${pe.clientHeight + 5}px)`;
            dd.style.width = `${input.clientWidth}px`;
        };

        input.insertAdjacentHTML("afterEnd", `<div id="${id}" class="drop-down-list"></div>`);
        input.onfocus = e => this.focus(e);
        input.onblur = e => this.blur(e);
        this.rszo = new ResizeObserver(move_dropdown);
        this.rszo.observe(input);
        this.input = input;
        this.self = document.querySelector(`#${id}`);
        this.self.input = input;
        this.updater = updater;
        this.state = 0;
        this.maybe_show();
        setTimeout(move_dropdown);
    }

    move_dropdown() {
        let dd = document.querySelector(`#${id}`);
        let pe = input.parentElement;
        dd.style.transform = `translate(0px, ${pe.clientHeight + 5}px)`;
        dd.style.width = `${input.clientWidth}px`;
    }

    maybe_show(show=true) {
        let visible = show && this.state && this.self.innerHTML.trim();
        this.self.style.opacity = visible ? "100%" : "0%";
        setTimeout(_ => { this.self.style.pointerEvents = visible ? "auto" : "none"; }, 300);
    }

    update(show=true) {
        this.updater(this.self, () => { this.maybe_show(show); });
    }

    blur(e) {
        this.state = 0;
        this.maybe_show();
    }

    focus(e) {
        this.state = 1;
        this.maybe_show();
    }
}

c6t_dialog.show = () => {
    const by_id = id => document.getElementById(id);
    const by_selector = sel => document.querySelector(sel);
    fetch('{% url "lms:c6t_form" %}').then(response => response.text()).then(html => {
        c6t_dialog.close();
        c6t_dialog.body().innerHTML = `<section class="on-narrow"><h1 class="mb1" style="text-align: center;">Ваш заказ</h1>{{separator}}</section>
<div class="grid-c6t">
    <section class="c6t-form-container">
    </section>
    <div class="c6t-scart-container items-top-down">
        <section class="c6t-sidebar">
        </section>
        <section id="c6t-status" class="on-wide c6t-status">
        </section>
    </div>
    <div class="c6t-button-container" style="display: flex; flex-flow: column;">
        <button id="c6t-submit-button" class="medium inverted" disabled="true" onclick="_form.onsubmit(null);">{{param_label_checkout}}</button>
    </div>
</div>`;
        c6t_dialog.form_container().innerHTML = html;

        __api_call__('{% url "api:get_customer_info" flags=15 %}', null, answer => {
            _form = by_id('c6t-form');
            _first_name = by_id('c6t-cu_first_name');
            _last_name = by_id('c6t-cu_last_name');
            _phone = by_id('c6t-cu_phone');
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
            _d6y_service_0.parentElement.insertAdjacentHTML('beforeEnd', `&nbsp;<span id='c6t-cd-info'></span>`);
            _d6y_service_1.parentElement.insertAdjacentHTML('beforeEnd', `&nbsp;<span id='c6t-pr-info'></span>`);
            _confirm.parentElement.style.flexFlow = "row-reverse";
            _confirm.parentElement.style.justifyContent = "start";
            _confirm.parentElement.style.alignContent = "center";

            _first_name.value = answer.first_name;
            _last_name.value = answer.last_name;
            _phone.value = answer.phone;
            _street.value = answer.address.street;
            _building.value = answer.address.building;
            _entrance.value = answer.address.entrance;
            _floor.value = answer.address.floor;
            _apartment.value = answer.address.apartment;
            _fullname.value = answer.address.fullname;

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

            const streets_updater = (holder, functor) => {
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                let url = '{% url "lms:c6t_info" kind="streets" data="datastr" %}'.replace(/\/datastr\/$/, `/${ds}/?city_uuid=${_city_uuid.value}&street=${_street.value}&building=${_building.value}&tid=${holder.input.id}`);
                fetch(url).then(response => response.text()).then(html => {
                    holder.innerHTML = html;
                    functor();
                }).catch(_ => {});
            }

            const buildings_updater = (holder, functor) => {
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                let url = '{% url "lms:c6t_info" kind="buildings" data="datastr" %}'.replace(/\/datastr\/$/, `/${ds}/?city_uuid=${_city_uuid.value}&street=${_street.value}&building=${_building.value}&tid=${holder.input.id}`);
                fetch(url).then(response => response.text()).then(html => {
                    holder.innerHTML = html;
                    functor();
                }).catch(_ => {});
            }

            const update_streets = (flag = true) => {
                let ready = c6t_dialog.ready();
                _street.dd.update(flag && ready && ready.value == 'yes' && _street.value);
            }

            const update_buildings = (flag = true) => {
                let ready = c6t_dialog.ready();
                _building.dd.update(flag && ready && ready.value == 'yes' && _street.value && _building.value);
            }

            const update_summary = () => {
                let c6t_status = by_id("c6t-status");
                if(c6t_status.controller) { c6t_status.controller.abort(); }
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                let url = '{% url "lms:c6t_info" kind="summary" data="dvservice" %}'.replace(/\/dvservice\/$/, `/${ds}/?city_uuid=${_city_uuid.value}&street=${_street.value}&building=${_building.value}`);
                c6t_status.controller = new AbortController();
                fetch(url, {signal: c6t_status.controller.signal}).then(response => response.text()).then(html => {
                    c6t_status.controller = null;
                    let statuses = document.querySelectorAll(".c6t-status");
                    statuses.forEach((status, arg1, arg2) => {
                        status.innerHTML = html;
                    });
                    setTimeout(() => {
                        update_streets();
                        update_buildings();
                    });
                }).catch(_=>{});
                fetch(`{% url "lms:c6t_info" kind="delivery" data="cd" %}?city_uuid=${_city_uuid.value}&street=${_street.value}&building=${_building.value}`)
                .then(response => response.text()).then(html => {
                    c6t_dialog.cd_info().innerHTML = html;
                }).catch(_=>{});
                fetch(`{% url "lms:c6t_info" kind="delivery" data="pr" %}?city_uuid=${_city_uuid.value}&street=${_street.value}&building=${_building.value}`)
                .then(response => response.text()).then(html => {
                    c6t_dialog.pr_info().innerHTML = html;
                }).catch(_=>{});
            };

            const city_chosen = () => !!_city_uuid.value;
            c6t_dialog.choose_city = (text, uuid, do_update_summary = true) => {
                _city_uuid.value = uuid;
                _city.value = text;
                if(text && uuid) { c6t_dialog.city_list().style.visibility = 'hidden'; }
                if(do_update_summary) { setTimeout(update_summary); }
            }

            const d6y_changed = () => {
                if(!city_chosen()) { setTimeout(update_cities); }
                setTimeout(update_summary);
            };

            _city.tmo_id = null;
            _city.oninput = _ => {
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

            _street.tmo_id = null;
            _street.oninput = _ => {
                update_buildings();
                if(_street.tmo_id) { clearTimeout(_street.tmo_id); }
                _street.tmo_id = setTimeout(() => {
                    update_summary();
                    update_streets();
                    _street.tmo_id = null;
                }, 1000);
            };
            
            _building.tmo_id = null;
            _building.oninput = _ => {
                if(_building.tmo_id) { clearTimeout(_building.tmo_id); }
                _building.tmo_id = setTimeout(() => {
                    update_summary();
                    update_buildings();
                    _building.tmo_id = null;
                }, 1000);
            };

            _d6y_service_0.onchange = d6y_changed;
            _d6y_service_1.onchange = d6y_changed;

            const filled = () => {
                let ready = c6t_dialog.ready();
                return ready &&
                    ready.value == 'yes' &&
                    _first_name.value &&
                    _last_name.value &&
                    _phone.value &&
                    _city_uuid.value &&
                    _city.value &&
                    _street.value &&
                    _building.value &&
                    _entrance.value &&
                    _floor.value &&
                    _apartment.value &&
                    _fullname.value &&
                    _confirm.checked
            };

            const check_filled = () => {
                if(filled()) c6t_dialog.button().removeAttribute("disabled");
                else c6t_dialog.button().setAttribute("disabled", "disabled");
            };

            _confirm.onchange = check_filled;

            _form.onsubmit = e => {
                if(e) e.preventDefault();
                let ds = by_selector('input[id^="c6t-d6y_service_"]:checked').value;
                __api_call__('{% url "api:c6t" %}', {
                    delivery: ds,
                    cu_first_name: _first_name.value,
                    cu_last_name: _last_name.value,
                    cu_phone: _phone.value,
                    cu_city_uuid: _city_uuid.value,
                    cu_city: _city.value,
                    cu_street: _street.value,
                    cu_building: _building.value,
                    cu_entrance: _entrance.value,
                    cu_floor: _floor.value,
                    cu_apartment: _apartment.value,
                    cu_fullname: _fullname.value,
                    cu_confirm: _confirm.checked
                }, result => {
                    if(result.success) {
                        window.location.href = result.redirect;
                    } else {
                        show_js_message(result.why);
                    }
                });
            }

            c6t_dialog.__on_scart_changed = e => fetch('{% url "lms:c6t_scart" %}').then(response => response.text()).then(html => {
                c6t_dialog.sidebar().innerHTML = html;
                update_summary();
            });

            window.addEventListener(EventType.SCART_CHANGED, c6t_dialog.__on_scart_changed);
            scart_changed();
            const mask = IMask(document.querySelector("input.telephone"), {mask: '{+7} (000) 000-00-00'});
            c6t_dialog.choose_city(answer.address.city, answer.address.city_uuid, false);
            d6y_changed({currentTarget: by_selector('input[id^="c6t-d6y_service_"]:checked')});
            c6t_dialog.rszo = new ResizeObserver(move_city_list);
            c6t_dialog.rszo.observe(_city);
            _street.dd = new Dropdown(_street, "c6t-dd-street", streets_updater);
            _building.dd = new Dropdown(_building, "c6t-dd-building", buildings_updater);
            c6t_dialog.sch = suppress_scrolling();
            c6t_dialog.iid = setInterval(check_filled, 1000);
            c6t_dialog.self().onclose = c6t_dialog.release;
            c6t_dialog.self().showModal();
        });
    });
};
