class {{name}} {
    constructor(input, id, updater, show_enabler, action = null) {
        let move_dropdown = _ => {
            let dd = document.querySelector(`#${id}`);
            let pe = input.parentElement;
            dd.style.transform = `translate(0px, ${pe.clientHeight + 5}px)`;
            dd.style.width = `${input.clientWidth}px`;
        };

        input.insertAdjacentHTML("afterEnd", `<div id="${id}" class="{{class}}"></div>`);
        input.onfocus = e => this.focus(e);
        input.onblur = e => this.blur(e);
        input.oninput = e => this.changed(e);
        input.onchange = e => this.changed(e);
        this.rszo = new ResizeObserver(move_dropdown);
        this.rszo.observe(input);
        this.input = input;
        this.self = document.querySelector(`#${id}`);
        this.self.input = input;
        this.updater = updater;
        this.show_enabler = show_enabler;
        this.action = action;
        this.state = 0;
        this.tmid = null;
        this.show_if_possible();
        setTimeout(move_dropdown);
    }
    show_if_possible() {
        let visible = this.show_enabler() && this.state && this.self.innerHTML.trim();
        this.self.style.opacity = visible ? "100%" : "0%";
        setTimeout(() => { this.self.style.pointerEvents = visible ? "auto" : "none"; }, 300);
    }
    update() {
        this.updater(this.self, () => { this.show_if_possible(); });
    }
    blur(e) {
        this.state = 0;
        this.show_if_possible();
    }
    focus(e) {
        this.state = 1;
        this.show_if_possible();
    }
    changed(e) {
        if(this.tmid) {
            clearTimeout(this.tmid);
        }
        this.tmid = setTimeout(() => {
            this.tmid = null;
            this.update();
            if (this.action) {
                this.action();
            }
        }, 500);
    }
}