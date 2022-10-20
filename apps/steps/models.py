from django.db import models

from apps.account.models import Participant
from apps.core.utils import get_report_image_path


class Step(models.Model):
    participant = models.ForeignKey(Participant, related_name='steps', on_delete=models.CASCADE)
    date = models.DateField('Дата')
    steps = models.PositiveIntegerField('Количество шагов')
    photo = models.ImageField('Фотоподтверждение', upload_to=get_report_image_path)

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шагов'
