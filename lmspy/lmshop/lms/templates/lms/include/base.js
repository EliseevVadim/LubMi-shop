const {{token}} = Cookies.get('csrftoken');
const __api_call__ = (url, obj, functor, method='POST', content_type='application/json') => {
    options = {
        method: method,
        headers: {
            'Content-Type': content_type,
            'X-CSRFToken': {{token}}
        },
        body: obj?JSON.stringify(obj):''
    }
    fetch(url, options)
        .then(response => response.json())
        .then(functor);
};

const ContentType = {
    NONE: 0,
    SCART: 1,
    FAVORITES: 2,
    NAVIGATION: 3
};

const EventType = {
    SCART_CHANGED: "ev_scart_changed",
};

function suppress_scrolling() {
    let sch = window.onscroll;
    let sx = window.scrollX;
    let sy = window.scrollY;
    window.onscroll = _ => {
        if(window.scrollX != sx || window.scrollY != sy) {
            setTimeout(() => window.scroll(sx, sy));
        }
    };
    return sch;
}

function release_scrolling(sch) {
    window.onscroll = sch ? sch : null;
}