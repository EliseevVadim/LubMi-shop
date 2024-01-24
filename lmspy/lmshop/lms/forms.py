from django import forms
from .models import NotificationRequest


class ShortCustomerInfoForm(forms.ModelForm):
    id = 'scui-form'
    title = 'Сообщить о поступлении товара'
    description = 'Выберите удобный способ для оповещения о повторном наличии данного товара'
    confirmation = "Получить уведомление"
    cancel = "🞨"

    class Meta:
        model = NotificationRequest
        fields = ['name', 'phone', 'email']
        labels = {
            "name": '',
            "phone": '',
            "email": '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'id': 'scui-name', 'placeholder': 'Как к Вам обращаться'}),
            'phone': forms.TextInput(attrs={'id': 'scui-phone', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'id': 'scui-email', 'placeholder': 'Почта'}),
        }
