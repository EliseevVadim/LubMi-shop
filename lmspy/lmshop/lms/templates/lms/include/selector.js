const customSelect = document.querySelector(".custom-select");
const selectBtn = document.querySelector(".select-button");
const selectedValue = document.querySelector(".selected-value");
const optionsList = document.querySelectorAll(".select-dropdown li");

selectBtn.addEventListener("click", () => {
    customSelect.classList.toggle("active");
    selectBtn.setAttribute(
        "aria-expanded",
        selectBtn.getAttribute("aria-expanded") === "true" ? "false" : "true");
});

optionsList.forEach((option) => {
    function handler(e) {
        if (e.type === "click" && e.clientX !== 0 && e.clientY !== 0) {
            selectedValue.textContent = this.children[1].textContent;
            selectedValue.textContent = this.children[0].name;
            customSelect.classList.remove("active");
        }
        if (e.key === "Enter") {
            selectedValue.textContent = this.textContent;
            customSelect.classList.remove("active");
        }
    }
    option.addEventListener("keyup", handler);
    option.addEventListener("click", handler);
});