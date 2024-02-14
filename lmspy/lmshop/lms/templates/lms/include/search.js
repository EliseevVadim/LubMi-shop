const sch = {
    dialog: () => document.querySelector('#sch-dialog'),
    box: () => document.querySelector('#sch-box'),
    text: () => document.querySelector('#sch-text'),
    result: () => document.querySelector('#sch-result'),
    footer: () => document.querySelector('#sch-footer'),
    open: () => {
        sch.dialog().classList.remove('full-screen');
        sch_dialog.show('{% url "lms:search" %}');
    },
    expand: () => {
        sch.footer().innerHTML = '<p>Кнопки</p>';
        sch.dialog().classList.add('full-screen');
    },
    collapse: () => {
        sch.footer().innerHTML = '';
        sch.dialog().classList.remove('full-screen');
    },
    tid: null,
    update: (text) => {
        if(sch.tid) { clearTimeout(sch.tid) }
        sch.tid = setTimeout(_ => {
            (text ? sch.expand : sch.collapse)();
            fetch('{% url "lms:index" %}'+'?page=1').then(response => response.text()).then(html => {
                sch.result().innerHTML = html;
            });
        }, text ? 1000 : 100);
    },

};
