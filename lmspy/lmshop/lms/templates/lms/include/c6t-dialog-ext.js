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
        // TODO prefill fields from CI
        c6t_dialog.self().showModal();
        scart_changed();
    });
};
