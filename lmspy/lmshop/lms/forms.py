from django import forms
from .models import CustomerShortInfo


class CustomerShortInfoForm(forms.ModelForm):
    title = 'Сообщить о поступлении товара'
    description = 'Выберите удобный способ для оповещения о повторном наличии данного товара'
    confirmation = "Получить уведомление"

    class Meta:
        model = CustomerShortInfo
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
