import datetime
from django.db import models
from django.db.models import signals, Sum
from django.utils.safestring import mark_safe

from apps.account.models import Participant
from apps.core.utils import get_report_image_path
from apps.steps.signals import check_individual_task_complete


class Step(models.Model):
    participant = models.ForeignKey(Participant, verbose_name="Участник", related_name='steps', on_delete=models.CASCADE)
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
    
    def plural(self, value):
        words = ["шаг", "шага", "шагов"]
        if 2 <= value % 10 <= 4 and not 12 <= value % 100 <= 14:
            return words[1]
        elif value % 10 == 1 and value % 100 != 11:
            return words[0]
        else:
            return words[2]
    
    def total(self):
        return Step.objects.aggregate(Sum('steps'))
    
    def total_today(self):
        return Step.objects.filter(date=datetime.date.today()).aggregate(Sum('steps'))
        

    photo_preview.short_description = 'Фотоотчёт'
    photo_preview_in_list.short_description = 'Фотоотчёт'


signals.post_save.connect(check_individual_task_complete, sender=Step)
