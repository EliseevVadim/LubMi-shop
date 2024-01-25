<script>
    let {{kind}}_page = 2;
    let {{kind}}_update = () => {
        fetch("?order={{order}}&kind={{kind}}&page=" + {{kind}}_page).then(response => response.text()).then(text => {
            document.getElementById("{{kind}}-list").insertAdjacentHTML('beforeEnd', text);
            if(++{{kind}}_page > {{pages}} || text === '') {
                document.getElementById("{{kind}}-upd-btn").style.visibility = 'hidden';
            }
        });
    };
</script>