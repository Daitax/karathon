import datetime

from django.db import models
from django.db.models import Sum, signals
from django.utils.safestring import mark_safe

from apps.account.models import Participant
from apps.core.utils import checking, get_report_image_path
from apps.steps.signals import check_individual_task_complete, check_screenshot


class Step(models.Model):
    participant = models.ForeignKey(
        Participant,
        verbose_name="Участник",
        related_name="steps",
        on_delete=models.CASCADE,
    )
    date = models.DateField("Дата")
    steps = models.PositiveIntegerField("Количество шагов")
    photo = models.ImageField(
        "Фотоподтверждение", upload_to=get_report_image_path
    )
    is_completed = models.BooleanField("Задание дня выполнено?", default=False)
    bonus = models.PositiveIntegerField(
        "Дополнительный бонус", blank=True, null=True
    )

    class Meta:
        ordering = ("-date",)
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"

    def __str__(self):
        return "Отчёт от {participant}".format(participant=self.participant)

    def photo_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" height="300" />'.format(self.photo.url)
            )
        return ""

    def photo_preview_in_list(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" height="100" />'.format(self.photo.url)
            )
        return ""

    def amount_matches_screenshot(self, steps, photo):
        # image_url = "karathon/media/" + get_report_image_path(
        #     participant, photo
        # )
        # image_url = str(photo.temporary_file_path())
        scale_coef = [0.25, 0.5, 1, 2, 3, 4, 5, 6]
        min_thresh = 10
        return checking(scale_coef, min_thresh, photo, steps)

    def total(self):
        return Step.objects.aggregate(Sum("steps"))

    def total_today(self):
        return Step.objects.filter(date=datetime.date.today()).aggregate(
            Sum("steps")
        )

    photo_preview.short_description = "Фотоотчёт"
    photo_preview_in_list.short_description = "Фотоотчёт"


signals.post_save.connect(check_individual_task_complete, sender=Step)
signals.post_save.connect(check_screenshot, sender=Step)
