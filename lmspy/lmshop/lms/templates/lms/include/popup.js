const show_popup = (text) => {
    document.querySelector("#{{popup_id}} span").textContent = text;
    document.getElementById('{{popup_id}}').style.visibility = "visible";
};
const hide_popup = () => {
    document.getElementById('{{popup_id}}').style.visibility = "hidden";
};

const popup = {
    self: () => document.getElementById('{{popup_id}}'),
    show: text => { document.querySelector("#{{popup_id}} span").textContent = text; popup.self().style.visibility = "visible"; },
    hide: () => { popup.self().style.visibility = "hidden"; },
};