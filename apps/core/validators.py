from datetime import date

from django.core.exceptions import ValidationError


def not_earlier_today(value):
    today = date.today()
    if value < today:
        raise ValidationError('Дата не может быть меньше сегодняшней')
