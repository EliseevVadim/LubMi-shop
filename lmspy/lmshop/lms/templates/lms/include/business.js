{% include "lms/include/undo.js" with unique="scart" %}

const pcard_like_click = (input, url) => {
    url = url.replace(/\/\d\/$/, `/${input.checked?1:0}/`);
    __api_call__(url, null, answer => {
        let selector = `input[type="checkbox"][data-ppk="${answer.ppk}"]`;
        let inputs = document.querySelectorAll(selector);
        inputs.forEach((input, arg1, arg2) => {
            input.checked = answer.like;
        });
        {% if param_value_show_popup_on_favorite.lower.strip == "yes" %}
        if(input.checked) {
            popup.show('{{param_message_product_is_favorite}}');
        }
        {% endif %}
        if(right_sidebar.visible() && right_sidebar.ctype == ContentType.FAVORITES)
            right_sidebar.show_favorites();
    });
};

const notify_delivery = ppk => {
    __api_call__('{% url "api:get_customer_info" flags=6 %}', null, answer => {
        cu_form = document.getElementById('scui-form');
        cu_phone = document.getElementById('scui-phone');
        const mask = IMask(cu_phone, {mask: '{+7} (000) 000-00-00'});
        cu_email = document.getElementById('scui-email');
        cu_phone.value = answer.phone;
        cu_email.value = answer.email;
        cu_email.oninput = _ => { if(cu_email.value) cu_phone.removeAttribute('required'); else cu_phone.setAttribute('required',''); }
        cu_phone.oninput = _ => { if(cu_phone.value) cu_email.removeAttribute('required'); else cu_email.setAttribute('required',''); }
        cu_form.onsubmit = e => {
            e.preventDefault();
            __api_call__('{% url "api:notify_me_for_delivery" %}', { phone: cu_phone.value, email: cu_email.value, ppk: ppk }, result => {
                if(result.success) {
                    ndd_dialog.close();
                    popup.show("Ваш запрос на уведомление о доставке товара успешно отправлен");
                } else {
                    popup.show("При отправке запроса возникли проблемы, попробуйте повторить отправку позже");
                }
            });
        }
        cu_email.oninput(null);
        cu_phone.oninput(null);
        ndd_dialog.sch = suppress_scrolling();
        ndd_dialog.self().onclose = ndd_dialog.release;
        ndd_dialog.self().showModal();
    });
}

const scart_changed = () => {
    let e = new CustomEvent(EventType.SCART_CHANGED);
    window.dispatchEvent(e);
};

const product_to_scart = (ppk, size_id, quantity, on_success=null) => {
    __api_call__('{% url "api:product_to_scart" %}', { ppk: String(ppk), size_id: Number(size_id), quantity: String(quantity) }, result => {
        if(result.success) {
            scart_changed();
            if(on_success) on_success();
        } else {
            popup.show(result.why);
        }
    });
};

const kill_product_in_scart = (ppk, product_title, size_id, size) => {
    __api_call__('{% url "api:kill_product_in_scart" %}', { ppk: String(ppk), size: String(size) }, result => {
        if(result.success) {
            scart_changed();
            scart_undo.start({{param_value_undo_period|default:5.9}} * 1000 / scart_undo.period(),
                u => {
                    if(u.alive()) {
                        let cds = u.countdowns();
                        let mss = u.messages();
                        let wgs = u.widgets();
                        if(wgs && mss && cds) {
                            let text = `{{param_label_you_removed}} &laquo;${product_title}&raquo;`;
                            let count = String(Math.floor(u.count/10));
                            for(let ms of mss) ms.innerHTML = text;
                            for(let cd of cds) cd.innerHTML = count;
                            for(let wg of wgs) wg.style.display = "grid";
                        }
                    }
                },
                u => {
                    let wgs = u.widgets();
                    if(wgs) for(let wg of wgs) { wg.style.display = "none"; }
                    let e = new CustomEvent(EventType.SCART_CHANGED);
                    window.dispatchEvent(e);
                },
                u => { product_to_scart(ppk, size_id, result.quantity); }
            );
        } else {
            popup.show(result.why);
        }
    });
};

const show_product_details = url => {
    left_sidebar.hide();
    right_sidebar.hide();
    gp_dialog.show(url, null, () => {
        if(size_selector) {
            function fun(sid) {
                if(sid != "-") __api_call__('{% url "api:product_size_quantity" %}', { ppk: document.querySelector("#selected-ppk").value, size: sid }, result => {
                    document.querySelector("#selected-size").value = sid;
                    let in_stock = result.success && result.quantity > 0;
                    document.querySelector("#gp-dialog .btn-to-scart").style.display = in_stock ? "inline-block" : "none";
                    document.querySelector("#gp-dialog .btn-notify-me").style.display = !in_stock ? "inline-block" : "none";
                    document.querySelector("#gp-dialog .not-in-stock").style.display = !in_stock ? "inline-block" : "none";
                });
            }
            fun(document.querySelector("#selected-size").value);
            size_selector.init(fun);
            gpd = document.querySelector("#gp-dialog");
            gpd.classList.add("idiotic-design");
            setTimeout(()=>{ gpd.scrollTop = 0; }, 10);
        }
    });
};

const do_checkout = () => {
    left_sidebar.hide();
    right_sidebar.hide();
    c6t_dialog.show();
}