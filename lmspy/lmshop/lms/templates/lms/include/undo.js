const {{unique}}_undo = {
    timer_id: null,
    count: null,
    time_action: null,
    final_action: null,
    undo_action: null,

    alive: () => !!{{unique}}_undo.timer_id,
    period: () => 100,
    start: (count, time_action, final_action, undo_action) => {
        {{unique}}_undo.stop();
        {{unique}}_undo.count = Number(count);
        {{unique}}_undo.time_action = time_action;
        {{unique}}_undo.final_action = final_action;
        {{unique}}_undo.undo_action = undo_action;
        {{unique}}_undo.timer_id = setInterval(() => {
            if({{unique}}_undo.count) {
                {{unique}}_undo.do_time();
                --{{unique}}_undo.count;
            } else {
                {{unique}}_undo.stop();
            }
        }, {{unique}}_undo.period());
    },
    stop: () => {
        if({{unique}}_undo.alive()) {
            clearInterval({{unique}}_undo.timer_id);
        }
        {{unique}}_undo.do_final();
        {{unique}}_undo.timer_id = null;
        {{unique}}_undo.count = null;
        {{unique}}_undo.time_action = null;
        {{unique}}_undo.final_action = null;
        {{unique}}_undo.undo_action = null;
    },
    do_action: action => {
        if(action) {
            action({{unique}}_undo);
        }
    },
    do_time: () => {{unique}}_undo.do_action({{unique}}_undo.time_action),
    do_final: () => {{unique}}_undo.do_action({{unique}}_undo.final_action),
    do_undo: () => { {{unique}}_undo.do_action({{unique}}_undo.undo_action); {{unique}}_undo.stop(); },
    widgets: () => document.querySelectorAll('*[id$="-undo-section"]'),
    messages: () => document.querySelectorAll('*[id$="-undo-message"]'),
    countdowns: () => document.querySelectorAll('*[id$="-undo-countdown"]'),
};