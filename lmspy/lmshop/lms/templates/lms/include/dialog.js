const {{unique}}_dialog = {
    self: () => { return document.querySelector("#{{dialog_id}}"); },
    {% if not custom_load %}show: url  => {
        fetch(url).then(response => response.text()).then(html => {
            document.querySelector("#{{dialog_id}} .dialog-body").innerHTML = html;
            document.querySelector("#{{dialog_id}}").showModal();
        });
    },{% endif %}
    close: () => { document.querySelector("#{{dialog_id}}").close(); },
};