const show_{{side}}_sidebar = url => {
    fetch(url).then(response => response.text()).then(html => {
        document.getElementById('{{side}}_sidebar_content').innerHTML = html;
        document.getElementById('_{{side}}_sidebar').style.visibility = 'visible';
    });
};

const hide_{{side}}_sidebar = () => {
    document.getElementById('_{{side}}_sidebar').style.visibility = "hidden";
};