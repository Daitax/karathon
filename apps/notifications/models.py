import pytz
import datetime

from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404

from apps.account.models import Participant, Winner
from apps.core.utils import print_month_ru


class NotificationTemplate(models.Model):
    key = models.CharField("Ключ", max_length=30)
    name = models.CharField("Название", max_length=40)
    header = models.CharField("Заголовок", max_length=100)
    text = models.CharField("Текст", max_length=200)

    class Meta:
        verbose_name = "Шаблон уведомления"
        verbose_name_plural = "Шаблоны уведомлений"

    def __str__(self):
        return self.name


class Notification(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    template = models.ForeignKey(
        NotificationTemplate, verbose_name="Шаблон", on_delete=models.CASCADE
    )
    header = models.CharField("Вставка в заголовок", max_length=100)
    text = models.CharField("Текст", max_length=200)
    date = models.DateTimeField("Дата и время", auto_now_add=True)
    is_viewed = models.BooleanField("Прочитано", default=False)

    class Meta:
        ordering = ("is_viewed", "-date")

    def datetime_creation(self):
        participant_timezone = self.participant.get_participant_timezone()

        participant_notification_datetime = self.date.astimezone(
            participant_timezone
        )

        # TODO разобраться с выводом месяца на русском языке методами python/django
        format_datetime = (
            participant_notification_datetime.strftime("%d")
            + " "
            + print_month_ru(participant_notification_datetime.strftime("%m"))
            + " "
            + participant_notification_datetime.strftime("%Y")
            + " | "
            + participant_notification_datetime.strftime("%H")
            + ":"
            + participant_notification_datetime.strftime("%M")
        )

        return format_datetime

    @classmethod
    def finished_individual_karathon(cls, karathon, winner):
        template = NotificationTemplate.objects.get(key="finished_individual_karathon")
        header = template.header.format(karathon_number=karathon.number)
        text = template.text.format(winner=winner)

        create_notification_list = list()
        karathon_participants = Participant.objects.filter(karathon=karathon).exclude(id=winner.participant.id)

        for participant in karathon_participants:
            instance = cls(
                participant=participant,
                template=template,
                header=header,
                text=text,
            )
            create_notification_list.append(instance)

        cls.objects.bulk_create(create_notification_list, 1000)

    @classmethod
    def winner_individual_karathon(cls, karathon, winner):
        template = NotificationTemplate.objects.get(key="winner_individual_karathon")
        text = template.text.format(karathon_number=karathon.number)

        cls.objects.create(
            participant=winner.participant,
            template=template,
            header=template.header,
            text=text
        )

    @staticmethod
    def task_today(participant, date, task):
        template = NotificationTemplate.objects.get(key="task_today")

        # TODO разобраться с выводом месяца на русском языке методами python/django
        format_date = (
            date.strftime("%d")
            + " "
            + print_month_ru(date.strftime("%m"))
            + " "
            + date.strftime("%Y")
            + " г."
        )

        header = template.header.format(format_date=format_date)

        addition = task.addition if task.addition else ""
        text = task.text_task(participant)
        format_text = template.text.format(task=text, addition=addition)

        Notification.objects.create(
            participant=participant,
            template=template,
            header=header,
            text=format_text,
        )

    @staticmethod
    def notification_from_template(participant, key):
        template = NotificationTemplate.objects.get(key=key)

        header = template.header
        text = template.text

        Notification.objects.create(
            participant=participant,
            template=template,
            header=header,
            text=text,
        )

    @staticmethod
    def success_message(participant):
        template = get_object_or_404(
            NotificationTemplate, key="success_message"
        )
        header = template.header
        name = (
            participant.first_name if participant.first_name else "Карафонец"
        )
        text = template.text.format(name=name)
        Notification.objects.create(
            participant=participant,
            template=template,
            header=header,
            text=text,
        )

    def not_viewed_amount(self):
        not_viewed_notification_list = Notification.objects.select_related(
            "participant"
        ).filter(participant=self.participant, is_viewed=False)
        if not_viewed_notification_list:
            return len(not_viewed_notification_list)
        return ""

    def next_page_exists(self):
        messages = Notification.objects.select_related("participant").filter(
            participant=self.participant
        )
        if (
            messages.count() == messages.filter(is_viewed=False).count()
            or messages.count() <= settings.MESSAGES_PER_PAGE
        ):
            return False
        return True
