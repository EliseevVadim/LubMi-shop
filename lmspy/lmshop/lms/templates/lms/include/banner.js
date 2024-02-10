const {{unique}}_banner = {
    self: () => document.querySelector("#banner-{{unique}}"),
    button: () => document.querySelector("#banner-{{unique}}  .banner-button"),
    slogan: () => document.querySelector("#banner-{{unique}}  .banner-slogan"),
    init: () => {
        im1 = new Image(); im1.src = '{{img_1}}';
        im2 = new Image(); im2.src = '{{img_2}}';
        svg_1 = `<svg width="5mm" height="5mm" viewBox="0 0 7 7">
                 <g><circle id="{{unique}}-switch-1" cx="3" cy="3" r="2.5" fill="#fff" stroke="#fff" stroke-width="0.25px"/></g></svg>`;
        svg_2 = `<svg width="5mm" height="5mm" viewBox="0 0 7 7">
                 <g><circle id="{{unique}}-switch-2" cx="3" cy="3" r="2.5" fill="#0000" stroke="#fff" stroke-width="0.25px"/></g></svg>`;
        const switch_action = (sw_on, sw_off, img, b_text, s_text, ref) => {
            return _ => {
                {{unique}}_banner.self().style['background-image'] = `url(${img})`;
                {{unique}}_banner.button().innerHTML = b_text;
                {{unique}}_banner.slogan().innerHTML = s_text;
                {{unique}}_banner.button().onclick = _ => { window.location.href = ref; };
                sw_on.attributes.fill.nodeValue = "#fff";
                sw_off.attributes.fill.nodeValue = "#0000";
            };
        }
        {{unique}}_banner.self().insertAdjacentHTML('beforeEnd', `<div class="banner-switch">${svg_1}${svg_2}</div>`);
        sw1 = document.querySelector('#{{unique}}-switch-1');
        sw2 = document.querySelector('#{{unique}}-switch-2');
        a1 = switch_action(sw1, sw2, '{{img_1}}', '{{button_1}}', '{{slogan_1}}', '{{ref_1}}');
        a2 = switch_action(sw2, sw1, '{{img_2}}', '{{button_2}}', '{{slogan_2}}', '{{ref_2}}');
        sw1.addEventListener('click', a1);
        sw2.addEventListener('click', a2);
        a1();
    },
};