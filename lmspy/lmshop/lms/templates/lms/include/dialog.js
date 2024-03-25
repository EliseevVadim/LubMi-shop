const {{unique}}_dialog = {
    sch: undefined,
    release: () => {
        {{unique}}_dialog.self().classList.remove("idiotic-design");
        if({{unique}}_dialog.sch !== undefined) {
            release_scrolling({{unique}}_dialog.sch);
            {{unique}}_dialog.sch = undefined;
        }
    },
    self: () => document.querySelector("#{{dialog_id}}"),
    visible: () => {{unique}}_dialog.self().style.visibility == "visible",
    body: () => document.querySelector("#{{dialog_id}} .dialog-body"),
    confirm_button: () => document.querySelector("#{{dialog_id}} .dialog-confirm-button"),
    {% if dynamic %}
    show: (url, on_confirm = null, on_show = null)  => {
        fetch(url).then(response => response.text()).then(html => {
            {{unique}}_dialog.close();
            {{unique}}_dialog.body().innerHTML = html;
            if(on_show) {
                on_show();
            }
            if(on_confirm) {
                let cb = {{unique}}_dialog.confirm_button();
                if(cb) {
                    {{unique}}_dialog.confirm_button().onclick = _ => {
                        setTimeout(on_confirm);
                        {{unique}}_dialog.close();
                    }
                }
            }
            {{unique}}_dialog.sch = suppress_scrolling();
            {{unique}}_dialog.self().onclose = {{unique}}_dialog.release;
            {{unique}}_dialog.self().showModal();
        });
    },
    {% endif %}
    close: () => {
        {% if dynamic %}
        {{unique}}_dialog.body().innerHTML = '';
        {% endif %}
        {{unique}}_dialog.self().close();
    }
};