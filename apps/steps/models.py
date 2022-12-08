from django.db import models
from django.db.models import signals
from django.utils.safestring import mark_safe

from apps.account.models import Participant
from apps.core.utils import get_report_image_path
from apps.steps.signals import check_individual_task_complete


class Step(models.Model):
    participant = models.ForeignKey(Participant, verbose_name="Участник", related_name='steps', \
                                    on_delete=models.CASCADE)
    date = models.DateField('Дата')
    steps = models.PositiveIntegerField('Количество шагов')
    photo = models.ImageField('Фотоподтверждение', upload_to=get_report_image_path)
    is_completed = models.BooleanField('Задание дня выполнено?', default=False)
    bonus = models.PositiveIntegerField('Дополнительный бонус', blank=True, null=True)

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'

    def __str__(self):
        return 'Отчёт от {participant}'.format(participant=self.participant)

    def photo_preview(self):
        if self.photo:
            return mark_safe('<img src="{}" height="300" />'.format(self.photo.url))
        return ""

    def photo_preview_in_list(self):
        if self.photo:
            return mark_safe('<img src="{}" height="100" />'.format(self.photo.url))
        return ""

    photo_preview.short_description = 'Фотоотчёт'
    photo_preview_in_list.short_description = 'Фотоотчёт'


signals.post_save.connect(check_individual_task_complete, sender=Step)
