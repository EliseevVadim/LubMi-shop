const show_popup = (text) => {
    document.querySelector("#{{popup_id}} span").textContent = text;
    document.getElementById('{{popup_id}}').style.visibility = "visible";
};
const hide_popup = () => {
    document.getElementById('{{popup_id}}').style.visibility = "hidden";
};