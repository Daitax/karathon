import datetime

from django.db import models
from django.db.models import Sum, signals, Q, F, Value
from django.db.models.functions import Concat
from django.utils.safestring import mark_safe

from apps.account.models import Participant
from apps.core.models import Karathon, CustomRecordsmans
from apps.core.utils import checking, get_report_image_path
# from apps.steps.signals import check_task_complete


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
    karathon = models.ForeignKey(
        Karathon,
        verbose_name="Карафон",
        related_name="steps",
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField("Задание дня выполнено", default=False)
    bonus = models.PositiveIntegerField(
        "Дополнительный бонус", blank=True, null=True
    )

    class Meta:
        ordering = ("-date",)
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"

    def __str__(self):
        return "Отчёт от {participant}".format(participant=self.participant)

    def amount_matches_screenshot(self, steps, photo):
        # image_url = "karathon/media/" + get_report_image_path(
        #     participant, photo
        # )
        # image_url = str(photo.temporary_file_path())
        scale_coef = [0.25, 0.5, 1, 2, 3, 4, 5, 6]
        min_thresh = 10
        return checking(scale_coef, min_thresh, photo, steps)

    @classmethod
    def get_champs_list(cls):
        site_champs = cls.objects.filter(steps__gte=100000).annotate(
            name=Concat(F('participant__first_name'), Value(' '), F('participant__last_name'))
        ).annotate(
            participant_photo=F('participant__photo')
        ).annotate(
            karathon_number=F('karathon__number')
        ).values('name', 'participant_photo', 'steps', 'karathon_number')

        custom_recordsmans = CustomRecordsmans.objects.all()

        union_queryset = site_champs.union(custom_recordsmans).order_by('-steps')

        return union_queryset

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

    def show_text_task(self):
        if self.participant.task_of_day(self.date):
            return self.participant.task_of_day(self.date).text_task(self.participant)
        else:
            return 'Задания нет'

    @classmethod
    def total(cls):
        return cls.objects.aggregate(Sum("steps"))

    @classmethod
    def total_today(cls):
        return cls.objects.filter(date=datetime.date.today()).aggregate(Sum("steps"))

    @classmethod
    def total_last_karathon(cls):
        last_karathon = Karathon.last_karathon()

        if last_karathon:
            steps = cls.objects.filter(karathon=last_karathon).filter(
                Q(date__gte=last_karathon.starts_at) & Q(date__lte=last_karathon.finished_at)).aggregate(Sum("steps"))

            return steps
        else:
            return {"steps__sum": 0}


    photo_preview.short_description = "Фотоотчёт"
    photo_preview_in_list.short_description = "Фотоотчёт"
    show_text_task.short_description = "Задание"


# signals.post_save.connect(check_task_complete, sender=Step)
# signals.post_save.connect(check_screenshot, sender=Step)
