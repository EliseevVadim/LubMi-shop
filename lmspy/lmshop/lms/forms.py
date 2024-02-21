from django import forms
from .models import NotificationRequest, Parameter, Order


class ShortCustomerInfoForm(forms.ModelForm):
    id = 'scui-form'
    title = Parameter.value_of('title_notify_product_arrival', 'Сообщить о поступлении товара')
    description = Parameter.value_of('label_choose_way_to_notify', 'Выберите удобный способ для оповещения о повторном наличии данного товара')
    confirmation = Parameter.value_of('label_send_request', 'Получить уведомление')

    class Meta:
        model = NotificationRequest
        fields = ['name', 'phone', 'email']
        labels = {
            "name": '',
            "phone": '',
            "email": '',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'scui-name',
                'placeholder': Parameter.value_of('pholder_indicate_your_name', 'Укажите, как к Вам обращаться')
            }),
            'phone': forms.TextInput(attrs={
                'id': 'scui-phone',
                'placeholder': Parameter.value_of('pholder_enter_your_phone', 'Введите Ваш номер телефона'),
                'pattern': Parameter.value_of('regex_phone_number', """^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$""")
            }),
            'email': forms.EmailInput(attrs={
                'id': 'scui-email',
                'placeholder': Parameter.value_of('pholder_enter_your_email', 'Введите Ваш email')
            }),
        }


class CheckoutForm(forms.ModelForm):
    id = 'c6t-form'
    title = Parameter.value_of('title_checkout', 'Оформление заказа')
    description = Parameter.value_of('message_enter_checkout_data', 'Введите данные, необходимые для оформления заказа')

    class Meta:
        model = Order
        fields = [
            'cu_name',
            'cu_phone',
            'cu_email',
            'cu_city_uuid',
            'cu_city',
            'delivery_service',
            'cu_fullname',
            'cu_street',
            'cu_building',
            'cu_apartment',
            'cu_entrance',
            'cu_floor',
            'cu_confirm',
        ]
        labels = {
            "cu_name": '',
            "cu_phone": '',
            "cu_email": '',
            'cu_city_uuid': '',
            'cu_city': 'Доставка',
            'delivery_service': '',
            'cu_fullname': 'Получатель',
            'cu_street': '',
            'cu_building': '',
            'cu_apartment': '',
            'cu_entrance': '',
            'cu_floor': '',
            'cu_confirm': Parameter.value_of('label_i_am_agree_pp', 'Я согласен/на с политикой конфиденциальности'),
        }
        widgets = {
            'cu_name': forms.TextInput(attrs={
                'id': 'c6t-cu_name',
                'placeholder': Parameter.value_of('pholder_indicate_your_name', 'Укажите, как к Вам обращаться')
            }),
            'cu_phone': forms.TextInput(attrs={
                'id': 'c6t-cu_phone',
                'placeholder': Parameter.value_of('pholder_enter_your_phone', 'Введите Ваш номер телефона'),
                'pattern': Parameter.value_of('regex_phone_number', """^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$""")
            }),
            'cu_email': forms.EmailInput(attrs={
                'id': 'c6t-cu_email',
                'placeholder': Parameter.value_of('pholder_enter_your_email', 'Введите Ваш email')
            }),
            'cu_city_uuid': forms.HiddenInput(attrs={
                'id': 'c6t-cu_city_uuid'
            }),
            'cu_city':  forms.TextInput(attrs={
                'id': 'c6t-cu_city',
                'placeholder': Parameter.value_of('pholder_city', 'Город')
            }),
            'delivery_service':  forms.RadioSelect(attrs={
                'id': 'c6t-d6y_service',
                'placeholder': Parameter.value_of('pholder_delivery_service', 'Вариант доставки')
            }),
            'cu_fullname':  forms.TextInput(attrs={
                'id': 'c6t-cu_fullname',
                'placeholder': Parameter.value_of('pholder_full_name', 'Фамилия, имя, отчество полностью')
            }),
            'cu_street':  forms.TextInput(attrs={
                'id': 'c6t-cu_street',
                'placeholder': Parameter.value_of('pholder_street', 'Улица')
            }),
            'cu_building':  forms.TextInput(attrs={
                'id': 'c6t-cu_building',
                'placeholder': Parameter.value_of('pholder_building', 'Дом')
            }),
            'cu_entrance': forms.TextInput(attrs={
                'id': 'c6t-cu_entrance',
                'placeholder': Parameter.value_of('pholder_entrance', 'Подъезд')
            }),
            'cu_floor':  forms.TextInput(attrs={
                'id': 'c6t-cu_floor',
                'placeholder': Parameter.value_of('pholder_floor', 'Этаж')
            }),
            'cu_apartment':  forms.TextInput(attrs={
                'id': 'c6t-cu_apartment',
                'placeholder': Parameter.value_of('pholder_apartment', 'Квартира/офис')
            }),
            'cu_confirm':  forms.CheckboxInput(attrs={
                'id': 'c6t-cu_confirm'
            }),
        }
        