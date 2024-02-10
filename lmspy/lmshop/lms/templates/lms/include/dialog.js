const {{unique}}_dialog = {
    self: () => document.querySelector("#{{dialog_id}}"),
    visible: () => {{unique}}_dialog.self().style.visibility == "visible",
    body: () => document.querySelector("#{{dialog_id}} .dialog-body"),
    {% if dynamic %}
    show: url  => {
        fetch(url).then(response => response.text()).then(html => {
            {{unique}}_dialog.close();
            {{unique}}_dialog.body().innerHTML = html;
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