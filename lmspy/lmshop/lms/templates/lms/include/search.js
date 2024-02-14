const sch = {
    dialog: () => document.querySelector('#sch-dialog'),
    box: () => document.querySelector('#sch-box'),
    text: () => document.querySelector('#sch-text'),
    info: () => document.querySelector('#sch-info'),
    result: () => document.querySelector('#sch-result'),
    footer: () => document.querySelector('#sch-footer'),
    open: () => {
        sch.dialog().classList.remove('full-screen');
        sch_dialog.show('{% url "lms:search" item="sch-box" %}');
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
    page: null,
    filter: null,
    update_elements: () => {
        if(sch.page && sch.filter) {
            fetch(`{% url "lms:search" item="sch-info" %}?page=${sch.page}&filter=${sch.filter}`).then(response => response.text()).then(html => {
                sch.info().innerHTML = html;
            });
            fetch(`{% url "lms:search" item="sch-page" %}?page=${sch.page}&filter=${sch.filter}`).then(response => response.text()).then(html => {
                sch.result().innerHTML = html;
            });
            fetch(`{% url "lms:search" item="sch-footer" %}?page=${sch.page}&filter=${sch.filter}`).then(response => response.text()).then(html => {
                sch.footer().innerHTML = html;
            });
        } else {
            sch.info().innerHTML = '';
            sch.result().innerHTML = '';
            sch.footer().innerHTML = '';
        }
    },
    update: (text) => {
        text = encodeURIComponent(text);
        if(sch.tid) { clearTimeout(sch.tid) }
        sch.tid = setTimeout(_ => {
            (text ? sch.expand : sch.collapse)();
            sch.filter = text ? text : null;
            sch.page = text ? 1 : null;
            sch.update_elements();
        }, text ? 1000 : 100);
    },
    go_page: page => {
        sch.page = page;
        sch.update_elements();
    },
    go_prev_page: () => {
        if(sch.page > 1) {
            sch.go_page(sch.page - 1);
        }
    },
    go_next_page: page_count => {
        if(sch.page < page_count) {
            sch.go_page(sch.page + 1);
        }
    },
};
