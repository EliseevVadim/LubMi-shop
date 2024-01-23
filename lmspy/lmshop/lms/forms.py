from django import forms
from .models import CustomerShortInfo


class CustomerShortInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerShortInfo
        fields = "__all__"
        labels = {"name": "Имя", "phone": "Телефон", "email": "E-mail"}
