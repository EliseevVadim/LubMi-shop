const {{unique}}_dialog = {
    self: () => { return document.querySelector("#{{dialog_id}}"); },
    {% if not custom_load %}show: url  => {
        fetch(url).then(response => response.text()).then(html => {
            document.querySelector("#{{dialog_id}} .dialog-body").innerHTML = html;
            {{unique}}_dialog.self().showModal();
        });
    },{% endif %}
    close: () => { {{unique}}_dialog.self().close(); },
};