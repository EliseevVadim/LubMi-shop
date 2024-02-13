const sch = {
    box: () => document.querySelector('#search-box'),
    text: () => document.querySelector('#search-text'),
    result: () => document.querySelector('#search-result'),
    open: () => {
        sch_dialog.show('{% url "lms:search" %}');
    },
    update: (text) => {
        fetch('{% url "lms:index" %}'+'?page=1').then(response => response.text()).then(html => {
            sch.result().innerHTML = html;
        });
    },
};
