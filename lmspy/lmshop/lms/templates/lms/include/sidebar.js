const {{side}}_sidebar = {
    sch: undefined,
    release: () => {
        if({{side}}_sidebar.sch !== undefined) {
            release_scrolling({{side}}_sidebar.sch);
            {{side}}_sidebar.sch = undefined;
        }
    },
    ctype: ContentType.NONE,
    self: () => document.getElementById('_{{side}}_sidebar'),
    content: () => document.getElementById('{{side}}_sidebar_content'),
    visible: () => {{side}}_sidebar.self().style.visibility == "visible",
    show: (url, ctype) => {
        fetch(url).then(response => response.text()).then(html => {
            {{side}}_sidebar.hide();
            {{side}}_sidebar.content().innerHTML = html;
            {{side}}_sidebar.self().style.visibility = 'visible';
            {{side}}_sidebar.self().style.opacity = 1.0;
            {{side}}_sidebar.ctype = ctype;
            {{side}}_sidebar.sch = suppress_scrolling();
            if(ctype == ContentType.SCART && !{{side}}_sidebar.__on_scart_changed) {
                {{side}}_sidebar.__on_scart_changed = e => { if({{side}}_sidebar.visible()) {{side}}_sidebar.show(url, ctype); };
                window.addEventListener(EventType.SCART_CHANGED, {{side}}_sidebar.__on_scart_changed);
            }
        });
    },
    hide: () => {
        {{side}}_sidebar.release();
        {{side}}_sidebar.content().innerHTML = '';
        {{side}}_sidebar.self().style.visibility = "hidden";
        {{side}}_sidebar.self().style.opacity = 0.0;
        {{side}}_sidebar.ctype = ContentType.NONE;
        if(!!{{side}}_sidebar.__on_scart_changed) {
            window.removeEventListener(EventType.SCART_CHANGED, {{side}}_sidebar.__on_scart_changed);
            {{side}}_sidebar.__on_scart_changed = null;
        }
    },
    show_scart: () => {{side}}_sidebar.show('{% url "lms:scart" %}', ContentType.SCART),
    show_favorites: () => {{side}}_sidebar.show('{% url "lms:favorites" %}', ContentType.FAVORITES),
    show_nav_menu: () => {{side}}_sidebar.show('{% url "lms:nav_menu" %}', ContentType.NAVIGATION),
    __on_scart_changed: null
};