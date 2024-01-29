const {{side}}_sidebar = {
    ctype: SbarContentType.NTHNG,
    self: () => { return document.getElementById('_{{side}}_sidebar'); },
    show: (url, ctype) => { fetch(url).then(response => response.text()).then(html => {
        document.getElementById('{{side}}_sidebar_content').innerHTML = html;
        {{side}}_sidebar.self().style.visibility = 'visible';
        {{side}}_sidebar.ctype = ctype;
    }); },
    visible: () => {{side}}_sidebar.self().style.visibility == "visible",
    hide: () => { {{side}}_sidebar.self().style.visibility = "hidden"; },
    show_scart: () => {{side}}_sidebar.show('{% url "lms:scart" %}', SbarContentType.SCART),
    show_favorites: () => {{side}}_sidebar.show('{% url "lms:favorites" %}', SbarContentType.FVRTS),
};