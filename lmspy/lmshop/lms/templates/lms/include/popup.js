const popup = {
    tmid: null,
    self: () => document.getElementById('{{popup_id}}'),
    free: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    tmids: [null, null, null, null, null, null, null, null, null, null],
    show: text => {
        var i = popup.free.shift();
        if(i != undefined) {
            document.querySelector(`#popup-${i} span`).textContent = text;
            document.querySelector(`#popup-${i}`).classList.add("active");
            popup.tmids[i] = setTimeout(function() { popup.hide(i); }, {{param_value_popup_show_time}});
        }
    },
    hide: (i) => {
        if(popup.tmids[i]) {
            clearTimeout(popup.tmids[i]);
            popup.tmids[i] = null;
        }
        popup.free.push(i);
        popup.free.sort();
        document.querySelector(`#popup-${i}`).classList.remove("active");
    },
};