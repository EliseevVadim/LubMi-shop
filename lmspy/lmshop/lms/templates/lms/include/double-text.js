const intro_click = e => {
    function switcher(t) {
        if(t.tagName == "SECTION") {
            t.style.display = "none";
            t.nextElementSibling.style.display = "block";
        } else {
            switcher(t.parentElement);
        }
    }
    switcher(e.target);
}