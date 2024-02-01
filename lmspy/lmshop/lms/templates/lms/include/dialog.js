const {{unique}}_dialog = {
    self: () => document.querySelector("#{{dialog_id}}"),
    body: () => document.querySelector("#{{dialog_id}} .dialog-body"),{% if not custom_load %}
    show: url  => {
        fetch(url).then(response => response.text()).then(html => {
            {{unique}}_dialog.close();
            {{unique}}_dialog.body().innerHTML = html;
            {{unique}}_dialog.self().showModal();
        });
    },
    {% endif %}close: () => {
        {{unique}}_dialog.body().innerHTML = '';
        {{unique}}_dialog.self().close();
    }
};