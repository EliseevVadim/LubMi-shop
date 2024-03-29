{% if pages %} let {{kind}}_order = "{{order}}"
let {{kind}}_page = 2;
let {{kind}}_update = () => {
    fetch(`{% url "lms:index" %}?order=${ {{kind}}_order }&kind={{kind}}&page=${ {{kind}}_page }`).then(response => response.text()).then(text => {
        document.getElementById("{{kind}}-list").insertAdjacentHTML('beforeEnd', text);
        if(++{{kind}}_page > {{pages}} || text === '') {
            document.getElementById("{{kind}}-upd-btn").style.visibility = 'hidden';
        }
    });
};
let {{kind}}_reorder = (ord) => {
    fetch(`{% url "lms:index" %}?order=${ {{kind}}_order = ord }&kind={{kind}}&page=1`).then(response => response.text()).then(text => {
        document.getElementById("{{kind}}-list").innerHTML = text;
        {{kind}}_page = 2;
        if({{pages}} > 1) {
            document.getElementById("{{kind}}-upd-btn").style.visibility = 'visible';
        }
    });
}; {% endif %}
