from django import forms
from .models import ShortCustomerInfo


class ShortCustomerInfoForm(forms.ModelForm):
    title = 'Сообщить о поступлении товара'
    description = 'Выберите удобный способ для оповещения о повторном наличии данного товара'
    confirmation = "Получить уведомление"
    cancel = "🞨"

    class Meta:
        model = ShortCustomerInfo
        fields = "__all__"
        labels = {
            "name": '',
            "phone": '',
            "email": '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Как к Вам обращаться'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Почта'}),
        }
