const show_{{unique}}_modal_dialog = url => {
    fetch(url).then(response => response.text()).then(html => {
        document.querySelector("#{{dialog_id}} .dialog-body").innerHTML = html;
        document.querySelector("#{{dialog_id}}").showModal();
    });
};

const close_{{unique}}_modal_dialog = () => {
    document.querySelector("#{{dialog_id}}").close();
};