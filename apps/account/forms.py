from django import forms

from .models import Participant, WinnerQuestionnaire


class AuthEmailForm(forms.Form):
    email = forms.EmailField(error_messages={
            'invalid': 'Введен неверный email',
            'required': 'Введите email'
        })

    error_messages = {
        'email': {
            'error_send': "Ошибка отправки сообщения",
        },
    }


class AuthCodeForm(forms.Form):
    email = forms.EmailField()
    code = forms.IntegerField()


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'instagram', 'email', 'timezone_offset',
                  'category', 'photo']


class WinnerQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = WinnerQuestionnaire
        fields = ['postcode', 'country', 'city', 'address', 'shirt_size', 'сharity_сategory']
