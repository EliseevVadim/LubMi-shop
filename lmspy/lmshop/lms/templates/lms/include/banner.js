const {{unique}}_banner = {
    animate: false,
    tmid: null,
    self: () => document.querySelector("#banner-{{unique}}"),
    button: () => document.querySelector("#banner-{{unique}}  .banner-button"),
    slogan: () => document.querySelector("#banner-{{unique}}  .banner-slogan"),
    init: () => {
        if(!{{unique}}_banner.self()) { return; }
        let pre_1 = document.createElement('link')
        let pre_2 = document.createElement('link')
            pre_1.href = '{{img_1}}'
            pre_2.href = '{{img_2}}'
            pre_1.rel = 'preload'
            pre_2.rel = 'preload'
            pre_1.as = 'image'
            pre_2.as = 'image'
        document.head.appendChild(pre_1)
        document.head.appendChild(pre_2)
        svg_1 = `<svg width="5mm" height="5mm" viewBox="0 0 7 7"><g><circle id="{{unique}}-switch-1" cx="3" cy="3" r="2.5" fill="#fff" stroke="#fff" stroke-width="0.25px"/></g></svg>`;
        svg_2 = `<svg width="5mm" height="5mm" viewBox="0 0 7 7"><g><circle id="{{unique}}-switch-2" cx="3" cy="3" r="2.5" fill="#0000" stroke="#fff" stroke-width="0.25px"/></g></svg>`;
        g_1 = `{% include "lms/include/gradient.html" with gradient=g1 %}`
        g_2 = `{% include "lms/include/gradient.html" with gradient=g2 %}`
        const switch_action = (sw_on, sw_off, img, b_text, s_text, grad, ref) => {
            let p = {{param_value_slideshow_period|default:"10000"}};
            return _ => {
                function swf() {
                    {{unique}}_banner.self().style['background-image'] = `${grad} url(${img})`;
                    {{unique}}_banner.button().innerHTML = b_text;
                    {{unique}}_banner.slogan().innerHTML = s_text;
                    {{unique}}_banner.button().onclick = _ => { window.location.href = ref; };
                    sw_on.attributes.fill.nodeValue = "#fff";
                    sw_off.attributes.fill.nodeValue = "#0000";
                }
                if({{unique}}_banner.animate) {
                    {{unique}}_banner.self().classList.add("decorated");
                    setTimeout(() => { swf(); {{unique}}_banner.self().classList.remove("decorated"); }, 1350);
                } else {
                    {{unique}}_banner.animate = true;
                    swf();
                }
                if({{unique}}_banner.tmid) clearTimeout({{unique}}_banner.tmid);
                {{unique}}_banner.tmid = setTimeout(() => {
                    {{unique}}_banner.tmid = null;
                    sw_off.dispatchEvent(new MouseEvent("click"));
                }, p/2);
            };
        }
        {{unique}}_banner.self().insertAdjacentHTML('beforeEnd', `<div class="banner-switch">${svg_1}${svg_2}</div>`);
        sw1 = document.querySelector('#{{unique}}-switch-1');
        sw2 = document.querySelector('#{{unique}}-switch-2');
        sa1 = switch_action(sw1, sw2, '{{img_1}}', '{{button_1}}', '{{slogan_1}}', g_1, '{{ref_1}}');
        sa2 = switch_action(sw2, sw1, '{{img_2}}', '{{button_2}}', '{{slogan_2}}', g_2, '{{ref_2}}');
        sw1.addEventListener('click', sa1);
        sw2.addEventListener('click', sa2);
        {% if show %}
        sa{{show}}(null);
        {% endif %}
    },
};