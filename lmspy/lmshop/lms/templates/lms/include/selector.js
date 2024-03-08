const {{unique}}_selector = {
    custom_select: () => document.querySelector("#{{unique}}-custom-select"),
    select_btn: () => document.querySelector("#{{unique}}-select-button"),
    selected_value: () => document.querySelector("#{{unique}}-selected-value"),
    options_list: () => document.querySelectorAll("#{{unique}}-select-dropdown li"),
    init: () => {
        {{unique}}_selector.select_btn().addEventListener("click", () => {
            {{unique}}_selector.custom_select().classList.toggle("active");
            {{unique}}_selector.select_btn().setAttribute("aria-expanded", {{unique}}_selector.select_btn().getAttribute("aria-expanded") === "true" ? "false" : "true");
        });

        {{unique}}_selector.options_list().forEach((option) => {
            function handler(e) {
                if (e.type === "click" && e.clientX !== 0 && e.clientY !== 0) {
                    {{unique}}_selector.selected_value().textContent = this.children[1].textContent;
                    {{unique}}_selector.selected_value().textContent = this.children[0].name;
                    {{unique}}_selector.custom_select().classList.remove("active");
                }
                if (e.key === "Enter") {
                    {{unique}}_selector.selected_value().textContent = this.textContent;
                    {{unique}}_selector.custom_select().classList.remove("active");
                }
            }
            option.addEventListener("keyup", handler);
            option.addEventListener("click", handler);
        });
    }
};

