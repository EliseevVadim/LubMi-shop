const {{side}}_sidebar = {
    ctype: ContentType.NONE,
    self: () => document.getElementById('_{{side}}_sidebar'),
    content: () => document.getElementById('{{side}}_sidebar_content'),
    visible: () => {{side}}_sidebar.self().style.visibility == "visible",
    show: (url, ctype) => { fetch(url).then(response => response.text()).then(html => {
        {{side}}_sidebar.content().innerHTML = html;
        {{side}}_sidebar.self().style.visibility = 'visible';
        {{side}}_sidebar.ctype = ctype;
        if(ctype == ContentType.SCART && !{{side}}_sidebar.__on_scart_changed) {
            {{side}}_sidebar.__on_scart_changed = e => { if({{side}}_sidebar.visible()) {{side}}_sidebar.show(url, ctype); };
            window.addEventListener(EventType.SCART_CHANGED, {{side}}_sidebar.__on_scart_changed);
        }
    }); },
    hide: () => {
        {{side}}_sidebar.content().innerHTML = '';
        {{side}}_sidebar.self().style.visibility = "hidden";
        {{side}}_sidebar.ctype = ContentType.NONE;
        if(!!{{side}}_sidebar.__on_scart_changed) {
            window.removeEventListener(EventType.SCART_CHANGED, {{side}}_sidebar.__on_scart_changed);
            {{side}}_sidebar.__on_scart_changed = null;
        }
    },
    show_scart: () => {{side}}_sidebar.show('{% url "lms:scart" %}', ContentType.SCART),
    show_favorites: () => {{side}}_sidebar.show('{% url "lms:favorites" %}', ContentType.FAVORITES),
    __on_scart_changed: null
};