from django import forms
from .models import Participant, WinnerQuestionnaire

from phonenumber_field.formfields import PhoneNumberField


class AuthPhoneForm(forms.Form):
    phone = PhoneNumberField(
        error_messages={
            # 'invalid': 'Введите корректный номер телефона',
            'invalid': 'Введен неверный номер',
            'required': 'Введите номер телефона'
        })


class AuthCodeForm(forms.Form):
    code = forms.IntegerField()
    phone = PhoneNumberField()


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'instagram', 'email', 'timezone_offset',
                  'category', 'photo']


class WinnerQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = WinnerQuestionnaire
        fields = ['postcode', 'country', 'city', 'address', 'shirt_size', 'сharity_сategory']
