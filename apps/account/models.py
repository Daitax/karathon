import datetime
import hashlib

import pytz
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import Category, Karathon, Task


class User(AbstractUser):
    pass


class Participant(User):
    TIMEZONES = (
        ('Europe/Moscow', 'Мск'),
        ('Europe/Samara', 'Мск+01'),
        ('Asia/Yekaterinburg', 'Мск+02'),
        ('Asia/Omsk', 'Мск+03'),
        ('Asia/Novosibirsk', 'Мск+04'),
        ('Asia/Irkutsk', 'Мск+05'),
        ('Asia/Yakutsk', 'Мск+06'),
        ('Asia/Vladivostok', 'Мск+07'),
        ('Asia/Sakhalin', 'Мск+08'),
        ('Asia/Kamchatka', 'Мск+09'),
        ('Europe/Kaliningrad', 'Мск-01'),
        ('Europe/London', 'Мск-02'),
        ('UTC', 'Мск-03'),
        ('Atlantic/Cape_Verde', 'Мск-04'),
        ('Atlantic/South_Georgia', 'Мск-05'),
        ('America/Buenos_Aires', 'Мск-06'),
        ('America/New_York', 'Мск-07'),
        ('America/Panama', 'Мск-08'),
        ('America/Edmonton', 'Мск-09'),
        ('America/Los_Angeles', 'Мск-10'),
        ('America/Anchorage', 'Мск-11'),
        ('America/Adak', 'Мск-12'),
        ('Pacific/Honolulu', 'Мск-13'),
        ('Pacific/Midway', 'Мск-14'),
    )

    user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE)
    middle_name = models.CharField('Отчество', max_length=20, blank=True)
    phone = PhoneNumberField('Номер телефона', unique=True)
    photo = models.ImageField('Аватарка', blank=True)
    instagram = models.URLField('Ссылка на инстаграм', blank=True)
    timezone = models.CharField(max_length=30, choices=TIMEZONES, default="Etc/GMT-3")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    karathon = models.ManyToManyField(Karathon, related_name='participant')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return '{last} {first} {middle}'.format(last=self.last_name, first=self.first_name, middle=self.middle_name)

    def get_active_karathon(self):
        try:
            participant_date = self.participant.get_participant_time()
            karathon = Karathon.objects.get(
                participant=self,
                starts_at__lte=participant_date,
                finished_at__gte=participant_date
            )

            return karathon

        except ObjectDoesNotExist:
            return False

    def get_participant_time(self):
        participant_timezone = pytz.timezone(self.timezone)
        # return participant_timezone.localize(datetime.datetime.now())
        return datetime.datetime.now(participant_timezone)

    def get_today_task(self):
        try:
            today_task = Task.objects.get(
                karathon=self.get_active_karathon(),
                category=self.category,
                date=self.get_participant_time()
            )

            return today_task

        except ObjectDoesNotExist:
            return None

    def is_today_report(self):
        try:
            from apps.steps.models import Step
            Step.objects.get(participant=self, date=self.get_participant_time())
            return True
        except ObjectDoesNotExist:
            return False


class Sms(models.Model):

    @staticmethod
    def check_code(request, code):
        cookie_code = request.COOKIES['code']
        hash_code = hashlib.md5(bytes(code))

        if cookie_code == hash_code.hexdigest():
            return True
        else:
            return False

    @staticmethod
    def send_code(phone, code):
        response = {'status': 'OK'}
        return response

    @staticmethod
    def set_cookie_code(response, code):
        expires = datetime.datetime.now() + datetime.timedelta(minutes=1)
        code_hash = hashlib.md5(bytes(code))
        response.set_cookie('code', code_hash.hexdigest(), expires=expires)
        return response
