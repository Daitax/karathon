from django import forms
from phonenumber_field.formfields import PhoneNumberField


class AddDesireForm(forms.Form):
    email = forms.EmailField(error_messages={
        'invalid': 'Введен неверный email',
        'required': 'Введите email'
    })
