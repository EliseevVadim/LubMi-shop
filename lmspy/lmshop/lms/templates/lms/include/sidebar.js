const hide_{{side}}_sidebar = () => {
    document.getElementById('_{{side}}_sidebar').style.visibility = "hidden";
};
const {{side}}_sidebar = {
    self: () => { return document.getElementById('_{{side}}_sidebar'); },
    show: url => { fetch(url).then(response => response.text()).then(html => {
        document.getElementById('{{side}}_sidebar_content').innerHTML = html;
        document.getElementById('_{{side}}_sidebar').style.visibility = 'visible';
    }); },
    hide: () => { document.getElementById('_{{side}}_sidebar').style.visibility = "hidden"; },
};