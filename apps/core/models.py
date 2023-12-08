import datetime

from django.db import models, transaction
from django.urls import reverse

from apps.core.utils import get_choice_value
from apps.core.validators import not_earlier_today


class Category(models.Model):
    name = models.CharField('Название категории', max_length=20, blank=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class CharityCategory(models.Model):
    name = models.CharField('Название категории благотворительности', max_length=150, blank=False)

    class Meta:
        verbose_name = 'Категория благотворительности'
        verbose_name_plural = 'Категории благотворительности'

    def __str__(self):
        return self.name


class Karathon(models.Model):
    TYPE = (
        ('individual', 'Индивидуальный'),
        ('team', 'Командный'),
    )

    number = models.PositiveIntegerField('Номер карафона', blank=False, unique=True)
    starts_at = models.DateField('Дата начала', blank=False, validators=[not_earlier_today])
    finished_at = models.DateField('Дата окончания', blank=False, validators=[not_earlier_today])
    type = models.CharField('Тип', choices=TYPE, max_length=10)
    video_presentation_link = models.CharField('Ссылка на видеопрезентацию на youtube',
                                               max_length=70,
                                               help_text="Введите ссылку на видеопрезентацию на youtube, "
                                                         "если она есть, в формате "
                                                         "\"https://www.youtube.com/embed/XxXxXxX\"",
                                               blank=True,
                                               null=True)
    is_presentation = models.BooleanField('Отображать видеопрезентацию', default=False)

    class Meta:
        verbose_name = 'Карафон'
        verbose_name_plural = 'Карафоны'

    def __str__(self):
        return str(self.number) + ' карафон' + ' (' + self.get_karathon_type_value() + ')'

    def save(self, *args, **kwargs):
        if not self.is_presentation:
            return super(Karathon, self).save(*args, **kwargs)
        with transaction.atomic():
            Karathon.objects.filter(
                is_presentation=True).update(is_presentation=False)
            return super(Karathon, self).save(*args, **kwargs)

    @staticmethod
    def not_finished_karathons(current_datetime=datetime.datetime.now()):
        karathons = Karathon.objects.filter(
            finished_at__gte=current_datetime
        )
        return karathons

    def get_karathon_type_value(self):
        return get_choice_value(self.TYPE, self.type)

    @classmethod
    def last_karathon(cls):
        return cls.objects.filter(finished_at__lt=datetime.datetime.today()).order_by('finished_at').last()

    def karathon_url(self):
        return reverse('core:karathon', args=[self.number])

    def is_ended_karathon(self):
        late_time_offset = -11

        offset = datetime.timedelta(hours=late_time_offset)
        late_timezone = datetime.timezone(offset)
        late_datetime_tz = datetime.datetime.now(late_timezone)
        late_datetime = datetime.datetime(
            year=late_datetime_tz.year,
            month=late_datetime_tz.month,
            day=late_datetime_tz.day,
            hour=late_datetime_tz.hour,
        )

        late_date = datetime.date(late_datetime.year, late_datetime.month, late_datetime.day)

        next_day_after_finished = self.finished_at + datetime.timedelta(days=1)

        if next_day_after_finished == late_date and late_datetime.hour == 0:
            return True

        return False
