{% include "lms/include/undo.js" %}
const pcard_like_click = (input, url) => {
    url = url.replace(/\/\d\/$/, `/${input.checked?1:0}/`);
    __api_call__(url, null, answer => {
        let selector = `input[type="checkbox"][data-ppk="${answer.ppk}"]`;
        let inputs = document.querySelectorAll(selector);
        inputs.forEach((input, arg1, arg2) => {
            input.checked = answer.like;
        });
        if(right_sidebar.visible() && right_sidebar.ctype == SbarContentType.FVRTS)
            right_sidebar.show_favorites();
    });
};
const notify_delivery = ppk => {
    __api_call__('{% url "api:get_customer_info" flags=7 %}', null, answer => {
        cu_form = document.getElementById('scui-form');
        cu_name = document.getElementById('scui-name');
        cu_phone = document.getElementById('scui-phone');
        cu_email = document.getElementById('scui-email');
        cu_name.value = answer.name;
        cu_phone.value = answer.phone;
        cu_email.value = answer.email;
        cu_email.oninput = _ => { if(cu_email.value) cu_phone.removeAttribute('required'); else cu_phone.setAttribute('required',''); }
        cu_phone.oninput = _ => { if(cu_phone.value) cu_email.removeAttribute('required'); else cu_email.setAttribute('required',''); }
        cu_form.onsubmit = e => {
            e.preventDefault();
            __api_call__('{% url "api:notify_me_for_delivery" %}', { name: cu_name.value, phone: cu_phone.value, email: cu_email.value, ppk: ppk }, result => {
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
        ndd_dialog.self().showModal();
    });
}
const product_to_scart = (ppk, size_id, quantity) => {
    __api_call__('{% url "api:product_to_scart" %}', { ppk: String(ppk), size_id: Number(size_id), quantity: String(quantity) }, result => {
        if(result.success) {
            gp_dialog.close();
            right_sidebar.show_scart();
        } else {
            popup.show(result.why);
        }
    });
}
const kill_product_in_scart = (ppk, product_title, size_id, size) => {
    __api_call__('{% url "api:kill_product_in_scart" %}', { ppk: String(ppk), size: String(size) }, result => {
        if(result.success) {
            if(right_sidebar.visible() && right_sidebar.ctype == SbarContentType.SCART) {
                right_sidebar.show_scart();
                undo.start({{param_value_undo_period}} * 1000 / undo.period(),
                    u => {
                        if(u.alive()) {
                            let cd = u.countdown();
                            let ms = u.message();
                            let wg = u.widget();
                            if(wg && ms && cd) {
                                ms.innerHTML = `{{param_label_you_removed}} &laquo;${product_title}&raquo;`;
                                cd.innerHTML = String(Math.floor(u.count/10));
                                wg.style.display = "block";
                            }
                        }
                    },
                    u => {
                        let wg = u.widget();
                        if(wg) { wg.style.display = "none"; }
                        right_sidebar.show_scart();
                    },
                    u => { product_to_scart(ppk, size_id, result.quantity); }
                );
            }
        } else {
            popup.show(result.why);
        }
    });
}
const show_product_details = url => {
    left_sidebar.hide();
    right_sidebar.hide();
    gp_dialog.show(url);
};