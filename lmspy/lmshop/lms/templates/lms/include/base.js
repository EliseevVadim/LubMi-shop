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
};

const EventType = {
    SCART_CHANGED: "ev_scart_changed",
};