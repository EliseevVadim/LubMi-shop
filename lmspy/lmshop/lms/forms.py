from django import forms
from .models import NotificationRequest, Parameter, Order


class ShortCustomerInfoForm(forms.ModelForm):
    id = 'scui-form'
    title = Parameter.value_of('title_notify_product_arrival', 'Сообщить о поступлении товара')
    description = Parameter.value_of('label_choose_way_to_notify', 'Выберите удобный способ для оповещения о повторном наличии данного товара')
    confirmation = Parameter.value_of('label_send_request', 'Получить уведомление')
    # cancel = "🞨"

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
    description = Parameter.value_of('label_choose_way_to_notify', 'Выберите удобный способ для оповещения о повторном наличии данного товара')
    confirmation = Parameter.value_of('label_checkout', 'Оформить заказ')

    class Meta:
        model = Order
        fields = ['cu_name', 'cu_phone', 'cu_email']
        labels = {
            "cu_name": '',
            "cu_phone": '',
            "cu_email": '',
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
        }
        