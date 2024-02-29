const popup = {
    tmid: null,
    self: () => document.getElementById('{{popup_id}}'),
    show: text => {
        if(popup.tmid) { clearTimeout(popup.tmid); }
        popup.tmid = setTimeout(()=>{ popup.tmid = null; popup.hide(); }, {{param_value_popup_show_time}});
        document.querySelector("#{{popup_id}} span").textContent = text; popup.self().style.visibility = "visible";
    },
    hide: () => { popup.self().style.visibility = "hidden"; },
};