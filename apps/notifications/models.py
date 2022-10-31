import pytz
from django.db import models

from apps.account.models import Participant
from apps.core.utils import print_month_ru


class NotificationTemplate(models.Model):
    key = models.CharField('Ключ', max_length=30)
    name = models.CharField('Название', max_length=40)
    header = models.CharField('Заголовок', max_length=100)
    text = models.CharField('Текст', max_length=200)

    class Meta:
        verbose_name = 'Шаблон уведомления'
        verbose_name_plural = 'Шаблоны уведомлений'

    def __str__(self):
        return self.name


class Notification(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    template = models.ForeignKey(NotificationTemplate, verbose_name='Шаблон', on_delete=models.CASCADE)
    header = models.CharField('Вставка в заголовок', max_length=100)
    text = models.CharField('Текст', max_length=200)
    date = models.DateTimeField('Дата и время', auto_now_add=True)
    is_viewed = models.BooleanField('Прочитано', default=False)

    def datetime_creation(self):
        participant_timezone = pytz.timezone(self.participant.timezone)
        participant_notification_datetime = self.date.astimezone(participant_timezone)

        # TODO разобраться с выводом месяца на русском языке методами python/django
        format_datetime = participant_notification_datetime.strftime('%d') + ' ' + \
            print_month_ru(participant_notification_datetime.strftime('%m')) + ' ' + \
            participant_notification_datetime.strftime('%Y') + ' | ' + \
            participant_notification_datetime.strftime('%H') + ":" + \
            participant_notification_datetime.strftime('%M')

        return format_datetime


    @staticmethod
    def task_today(participant, date, task):
        template = NotificationTemplate.objects.get(key='task_today')

        # TODO разобраться с выводом месяца на русском языке методами python/django
        format_date = date.strftime('%d') + ' ' + print_month_ru(date.strftime('%m')) + ' ' + \
                      date.strftime('%Y') + ' г.'

        header = template.header.format(format_date=format_date)

        addition = task.addition if task.addition else ''
        text = template.text.format(task=task.task, addition=addition)

        Notification.objects.create(
            participant=participant,
            template=template,
            header=header,
            text=text,
        )

    @staticmethod
    def link_to_instagram(participant):
        template = NotificationTemplate.objects.get(key='link_to_instagram')

        header = template.header
        text = template.text

        Notification.objects.create(
            participant=participant,
            template=template,
            header=header,
            text=text,
        )

    @staticmethod
    def link_to_email(participant):
        template = NotificationTemplate.objects.get(key='link_to_email')

        header = template.header
        text = template.text

        Notification.objects.create(
            participant=participant,
            template=template,
            header=header,
            text=text,
        )
