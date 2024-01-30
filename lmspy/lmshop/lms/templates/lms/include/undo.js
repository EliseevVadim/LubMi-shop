const undo = {
    timer_id: null,
    count: null,
    time_action: null,
    final_action: null,
    undo_action: null,

    alive: () => !!undo.timer_id,
    start: (count, time_action, final_action, undo_action) => {
        undo.stop();
        undo.count = Number(count);
        undo.time_action = time_action;
        undo.final_action = final_action;
        undo.undo_action = undo_action;
        undo.timer_id = setInterval(() => {
            if(undo.count) {
                undo.do_time();
                --undo.count;
            } else {
                undo.stop();
            }
        }, 100);
    },
    stop: () => {
        if(undo.alive()) {
            clearInterval(undo.timer_id);
        }
        undo.do_final();
        undo.timer_id = null;
        undo.count = null;
        undo.time_action = null;
        undo.final_action = null;
        undo.undo_action = null;
    },
    do_action: action => {
        if(action) {
            action(undo);
        }
    },
    do_time: () => undo.do_action(undo.time_action),
    do_final: () => undo.do_action(undo.final_action),
    do_undo: () => { undo.do_action(undo.undo_action); undo.stop(); },
    widget: () => document.querySelector('#undo-section'),
    message: () => document.querySelector('#undo-message'),
    countdown: () => document.querySelector('#undo-countdown'),
};