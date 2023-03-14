import datetime
import hashlib

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import signals
from phonenumber_field.modelfields import PhoneNumberField

from apps.account.signals import send_new_participant_notifications
from apps.core.models import Category, Karathon, CharityCategory
from apps.core.utils import get_participant_photo_path


class User(AbstractUser):
    pass


class Participant(User):
    # TODO Удалить временные зоны с регионами
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
        ('America/Winnipeg', 'Мск-08'),
        ('America/Edmonton', 'Мск-09'),
        ('America/Los_Angeles', 'Мск-10'),
        ('America/Anchorage', 'Мск-11'),
        ('America/Adak', 'Мск-12'),
        ('Pacific/Honolulu', 'Мск-13'),
        ('Pacific/Midway', 'Мск-14'),
    )

    TIMEZONES_OFFSET = (
        ('+3', 'Мск'),
        ('+4', 'Мск+01'),
        ('+5', 'Мск+02'),
        ('+6', 'Мск+03'),
        ('+7', 'Мск+04'),
        ('+8', 'Мск+05'),
        ('+9', 'Мск+06'),
        ('+10', 'Мск+07'),
        ('+11', 'Мск+08'),
        ('+12', 'Мск+09'),
        ('+2', 'Мск-01'),
        ('+1', 'Мск-02'),
        ('0', 'Мск-03'),
        ('-1', 'Мск-04'),
        ('-2', 'Мск-05'),
        ('-3', 'Мск-06'),
        ('-4', 'Мск-07'),
        ('-5', 'Мск-08'),
        ('-6', 'Мск-09'),
        ('-7', 'Мск-10'),
        ('-8', 'Мск-11'),
        ('-9', 'Мск-12'),
        ('-10', 'Мск-13'),
        ('-11', 'Мск-14'),
    )

    user = models.OneToOneField(User, parent_link=True, on_delete=models.CASCADE)
    middle_name = models.CharField('Отчество', max_length=20, blank=True)
    phone = PhoneNumberField('Номер телефона', unique=True)
    photo = models.ImageField('Аватарка', blank=True, upload_to=get_participant_photo_path)
    instagram = models.URLField('Ссылка на инстаграм', blank=True)
    timezone = models.CharField(max_length=30, choices=TIMEZONES, default='Europe/Moscow')
    timezone_offset = models.CharField(max_length=3, choices=TIMEZONES_OFFSET, default='+3')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    karathon = models.ManyToManyField(Karathon, related_name='participant')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return '{last} {first} {middle} ({phone})'.format(last=self.last_name, first=self.first_name,
                                                          middle=self.middle_name, phone=self.phone)

    def best_steps_all(self):
        from apps.steps.models import Step
        best_steps = Step.objects.filter(participant=self).order_by('-steps').first()

        if best_steps:
            return best_steps.steps
        return False

    def best_steps_karathon(self):
        from apps.steps.models import Step
        best_steps = Step.objects.filter(
            participant=self,
            date__gte=self.get_active_karathon().starts_at,
            date__lte=self.get_active_karathon().finished_at
        ).order_by('-steps').first()
        if best_steps:
            return int(best_steps.steps)
        return False

    # TODO Сделать вывод участников желаемой команды в столбик
    def desirer_team(self):
        from apps.teams.models import DesiredTeam
        team = DesiredTeam.objects.filter(desirer=self)

        return [team_item.desired_participant.__str__() for team_item in team]

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
            return None

    def get_participant_time(self):
        participant_offset = datetime.timedelta(hours=int(self.timezone_offset))
        participant_timezone = datetime.timezone(participant_offset)
        return datetime.datetime.now(participant_timezone)
        # participant_timezone = pytz.timezone(self.timezone)
        # return datetime.datetime.now(participant_timezone)

    def is_today_report(self):
        try:
            from apps.steps.models import Step
            Step.objects.get(participant=self, date=self.get_participant_time())
            return True
        except ObjectDoesNotExist:
            return False

    def today_task(self):
        karathon = self.get_active_karathon()
        if karathon:
            if karathon.type == "individual":
                try:
                    from apps.tasks.models import IndividualTask
                    today_task = IndividualTask.objects.get(karathon=karathon, category=self.category,
                                                            date=self.get_participant_time())
                    return today_task
                except ObjectDoesNotExist:
                    return None

            elif karathon.type == "team":
                pass
        return None

if not settings.IS_TESTING:
    signals.post_save.connect(send_new_participant_notifications, sender=Participant)


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


class Winner(models.Model):
    karathon = models.ForeignKey(Karathon, verbose_name="Карафон", on_delete=models.SET_NULL, null=True, blank=False)
    participant = participant = models.ForeignKey(Participant, verbose_name="Участник", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Победитель'
        verbose_name_plural = 'Победители'

    def __str__(self):
        return self.participant

    def is_winner_participant(self):
        return Winner.objects.filter(participant=self.participant).exists()

    @staticmethod
    def set_individual_karathon_winner(karathon):
        print(1)
        print('Устанавливаем победителя индивидуального карафона:')
        print(karathon)
        print(2)

    @staticmethod
    def set_team_karathon_winners(karathon):
        print(1)
        print('Устанавливаем победителей командного карафона:')
        print(karathon)
        print(2)


class WinnerQuestionnaire(models.Model):
    SIZES = (
        ('xxs', 'xxs'),
        ('xs', 'xs'),
        ('s', 's'),
        ('m', 'm'),
        ('l', 'l'),
        ('xl', 'xl'),
        ('xxl', 'xxl'),
        ('3xl', '3xl'),
        ('4xl', '4xl'),
    )

    participant = models.ForeignKey(Participant, verbose_name="Участник", on_delete=models.CASCADE)
    postcode = models.CharField('Почтовый индекс', max_length=10)
    country = models.CharField('Страна', max_length=100)
    city = models.CharField('Населенный пункт', max_length=100)
    address = models.CharField('Населенный пункт', max_length=200)
    shirt_size = models.CharField('размер футболки', max_length=5, choices=SIZES, default='Europe/Moscow')
    сharity_сategory = models.ForeignKey(CharityCategory, verbose_name='Категория благотворительности',
                                         on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
