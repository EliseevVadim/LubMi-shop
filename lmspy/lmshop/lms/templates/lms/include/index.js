const pcard_like_click = (input, url) => {
  url = url.replace(/\/\d\/$/, `/${input.checked?1:0}/`);
  fetch(url, {'method': 'POST', headers: {'X-CSRFToken': csrftoken}}).then(response => response.json()).then(answer => {
    let selector = `input[type="checkbox"][data-ppk="${answer.ppk}"]`;
    let inputs = document.querySelectorAll(selector);
    inputs.forEach((input, arg1, arg2) => {
      input.checked = answer.like;
    });
  });
}
const notify_delivery = ppk => {
  fetch('{% url "api:get_customer_info" flags=7 %}', {method: 'POST', headers: {'X-CSRFToken': csrftoken}}).then(response => response.json()).then(answer => {
    dialog = document.getElementById('notify-delivery-dialog');
    cu_form = document.getElementById('scui-form');
    cu_name = document.getElementById('scui-name');
    cu_phone = document.getElementById('scui-phone');
    cu_email = document.getElementById('scui-email');
    cu_name.value = answer.name;
    cu_phone.value = answer.phone;
    cu_email.value = answer.email;
    cu_email.oninput = _ => { if(cu_email.value) cu_phone.removeAttribute('required'); else cu_phone.setAttribute('required',''); }
    cu_phone.oninput = _ => { if(cu_phone.value) cu_email.removeAttribute('required'); else cu_email.setAttribute('required',''); }
    cu_form.onsubmit = e => {
      e.preventDefault();
      fetch('{% url "api:notify_me_for_delivery" %}',
            { method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
              body: JSON.stringify({name: cu_name.value, phone: cu_phone.value, email: cu_email.value, ppk: ppk})
            }).then(response => response.json()).then(result => {
              if(result.ok) {
                dialog.close();
                show_popup("Ваш запрос на уведомление о доставке товара успешно отправлен");
              } else {
                show_popup("При отправке запроса возникли проблемы, попробуйте повторить отправку позже");
              }
            });
    }
    cu_email.oninput(null);
    cu_phone.oninput(null);
    dialog.showModal();
  });
}