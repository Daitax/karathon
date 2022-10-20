from django import forms
from .models import Step


class ReportForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['steps', 'photo']

        error_messages = {
            'steps': {
                'required': 'Введите количество шагов',
            },
            'photo': {
                'required': 'Прикрепите фото',
            },
        }
