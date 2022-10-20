from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from apps.core.utils import get_choice_value
from apps.core.validators import not_earlier_today


class Category(models.Model):
    name = models.CharField('Название категории', max_length=20, blank=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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

    class Meta:
        verbose_name = 'Карафон'
        verbose_name_plural = 'Карафоны'

    def __str__(self):
        return str(self.number) + ' карафон' + ' (' + self.get_karathon_type_value() + ')'

    def get_karathon_type_value(self):
        return get_choice_value(self.TYPE, self.type)


class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    karathon = models.ForeignKey(Karathon, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField('Дата', blank=False, validators=[not_earlier_today])
    task = models.CharField('Задание', max_length=200, blank=False)
    addition = models.CharField('Дополнение к заданию', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.task

    def clean(self):
        karathons = Karathon.objects.filter(starts_at__lte=self.date, finished_at__gte=self.date)
        if karathons.count() == 0:
            raise ValidationError({'date': 'На указанную дату карафонов нет'})

        try:
            karathons.get(number=self.karathon.number)
        except ObjectDoesNotExist:
            raise ValidationError({'karathon': 'На указанную дату карафона с таким номером нет'})

        # TODO Подумать реализацию проверки наличия задания на текущую дату в этой категории, и что бы не выбивало
        #  ошибку при редактировании

        # try:
        #     Task.objects.get(date=self.date, category=self.category)
        #     raise ValidationError({'category': 'На указанную дату карафона в этой категории уже есть задание'})
        # except ObjectDoesNotExist:
        #     pass
