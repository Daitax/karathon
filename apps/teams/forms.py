from django import forms
from phonenumber_field.formfields import PhoneNumberField


class AddDesireForm(forms.Form):
    phone = PhoneNumberField(
        error_messages={
            'invalid': 'Введите корректный номер телефона',
            'required': 'Введите номер телефона'
        })
