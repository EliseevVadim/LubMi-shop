const {{unique}}_banner = {
    current: undefined,
    tmid: null,
    self: () => document.querySelector("#banner-{{unique}}"),
    button: () => document.querySelector("#banner-{{unique}} .banner-button"),
    slogan: () => document.querySelector("#banner-{{unique}} .banner-slogan"),
    w_slogan: () => document.querySelector("#banner-{{unique}} .banner-slogan.on-wide"),
    n_slogan: () => document.querySelector("#banner-{{unique}} .banner-slogan.on-narrow"),
    init: () => {
        if(!{{unique}}_banner.self()) { return; }

        let pre_1 = document.createElement('link');
        let pre_2 = document.createElement('link');
        pre_1.href = '{{img_1}}';
        pre_2.href = '{{img_2}}';
        pre_1.rel = 'preload';
        pre_2.rel = 'preload';
        pre_1.as = 'image';
        pre_2.as = 'image';
        document.head.appendChild(pre_1);
        document.head.appendChild(pre_2);

        svg_1 = `<svg width="5mm" height="5mm" viewBox="0 0 7 7"><g><circle id="{{unique}}-switch-1" cx="3" cy="3" r="2.5" fill="#fff" stroke="#fff" stroke-width="0.25px"/></g></svg>`;
        svg_2 = `<svg width="5mm" height="5mm" viewBox="0 0 7 7"><g><circle id="{{unique}}-switch-2" cx="3" cy="3" r="2.5" fill="#0000" stroke="#fff" stroke-width="0.25px"/></g></svg>`;
        g_1 = `{% include "lms/include/gradient.html" with gradient=g1 %}`
        g_2 = `{% include "lms/include/gradient.html" with gradient=g2 %}`
        const switch_action = (rtl, sw_on, sw_off, img1, img2, b_text, ws_text, ns_text, grad, ref) => {
            let p = {{param_value_slideshow_period|default:"20"}} * 1000;
            let banner = {{unique}}_banner.self();
            return _ => {
                function swf() {
                    {{unique}}_banner.current = sw_on;
                    banner.style['background-image'] = `url(${img1}), url(${img2})`;
                    banner.style['background-position'] = rtl ? `center top, -200vw top` : `center top, 100vw top`;
                    banner.style['background-size'] = `cover, cover`;
                    {{unique}}_banner.button().innerHTML = b_text;
                    {{unique}}_banner.w_slogan().innerHTML = ws_text;
                    {{unique}}_banner.n_slogan().innerHTML = ns_text;
                    {{unique}}_banner.button().onclick = _ => { window.location.href = ref; };
                    sw_on.attributes.fill.nodeValue = "#fff";
                    sw_off.attributes.fill.nodeValue = "#0000";
                    let b = {{unique}}_banner.self();
                    setTimeout(() => {
                        banner.classList.remove("animated");
                        banner.style['background-image'] = grad ? `${grad}, url(${img1})` : `url(${img1})`;
                        banner.style['background-position'] = `center top`;
                        banner.style['background-size'] = `cover`;
                    }, 510);
                }
                if({{unique}}_banner.current && {{unique}}_banner.current != sw_on) {
                    banner.style['background-image'] = `url(${img1}), url(${img2})`;
                    banner.style['background-size'] = `cover, cover`;
                    banner.style['background-position'] = rtl ? `100vw top, center top` : `-200vw top, center top`;
                    setTimeout(() => {
                        {{unique}}_banner.self().classList.add("animated");
                        swf();
                    }, 25);
                } else {
                    swf();
                }
                if({{unique}}_banner.tmid) clearTimeout({{unique}}_banner.tmid);
                {{unique}}_banner.tmid = setTimeout(() => {
                    {{unique}}_banner.tmid = null;
                    sw_off.dispatchEvent(new MouseEvent("click"));
                }, p);
            };
        }
        {{unique}}_banner.self().insertAdjacentHTML('beforeEnd', `<div class="banner-switch">${svg_1}${svg_2}</div>`);
        sw1 = document.querySelector('#{{unique}}-switch-1');
        sw2 = document.querySelector('#{{unique}}-switch-2');
        sa1 = switch_action(false, sw1, sw2, '{{img_1}}', '{{img_2}}', '{{button_1}}', '{{w_slogan_1}}', '{{n_slogan_1}}', g_1, '{{ref_1}}');
        sa2 = switch_action(true, sw2, sw1, '{{img_2}}', '{{img_1}}', '{{button_2}}', '{{w_slogan_2}}', '{{n_slogan_2}}', g_2, '{{ref_2}}');
        sw1.addEventListener('click', sa1);
        sw2.addEventListener('click', sa2);
        sa{{show}}(null);
    },
};