const show_js_message = text => {
    url = '{% url "lms:js_message" message="@" %}'.replace(/\/@\/$/, `/${text}/`);
    msg_dialog.show(url, ()=>{});
}