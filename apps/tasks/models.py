import datetime

from django.db import models

# Create your models here.
from apps.account.models import Participant
from apps.core.models import Category, Karathon
from apps.core.validators import not_earlier_today


class IndividualTask(models.Model):
    TYPE = (
        ("walk_steps", "Пройти S шагов"),
        ("double_best", "Удвоить лучший результат или S шагов"),
        ("double_result_day", "Удвоить результат дня D или S шагов"),
        ("improve_best", "Улучшить лучший результат или S шагов"),
        ("improve_result_day", "Улучшить результат дня D или S шагов"),
        ("add_steps_to_day", "Добавить S шагов ко дню D"),
        ("palindrome", "Зеркалка"),
        ("steps_of_consecutive_digits", "Число шагов из последовательных цифр"),
        ("steps_multiple_number", "Число шагов, кратное N"),
        ("add_steps_to_report_digit", "Добавить X-тысяч шагов, где X - цифра в отчёте дня D, занимающая позицию P"),
        ("best_personal_record", "Побить личный рекорд или S шагов"),
    )

    category = models.ForeignKey(Category, verbose_name="Категория участника", on_delete=models.SET_NULL, null=True,
                                                                                                        blank=True)
    karathon = models.ForeignKey(Karathon, verbose_name="Карафон", on_delete=models.CASCADE)
    date = models.DateField('Дата', blank=False, validators=[not_earlier_today])
    type = models.CharField('Тип', max_length=100, choices=TYPE)
    steps = models.PositiveIntegerField('Количество шагов в задании (S)', null=True, blank=True, default=10000)
    task_date_report = models.DateField('День с какого берем шаги (D)',
                                        default=datetime.date.today() - datetime.timedelta(days=1), null=True,
                                        blank=True)
    multiple_number = models.PositiveIntegerField('Кол-во шагов, кратное этому числу (N)', null=True, blank=True,
                                                  default=5)
    position = models.PositiveIntegerField('Позиция цифры в отчёте (P)', default=1, null=True, blank=True)
    addition = models.CharField('Дополнение к заданию', max_length=200, null=True, blank=True)
    bonus = models.PositiveIntegerField('Бонус за выполнение задания')

    class Meta:
        verbose_name = 'Индивидуальное задание'
        verbose_name_plural = 'Индивидуальные задания'

    def __str__(self):
        return "Задание для {category} на {date}".format(category=self.category, date=self.date)

    def text_individual_task(self, participant):
        match self.type:
            case "walk_steps":
                text = "Пройдите {steps} шагов".format(steps=self.steps)
                return text
            case "double_best":
                text = "Удвойте Ваш лучший результат или пройдите {steps} шагов. (Ваш лучший результат: {" \
                       "best})".format(steps=self.steps, best=15131)
                return text
            case "double_result_day":
                pass
            case "improve_best":
                pass
            case "improve_result_day":
                pass
            case "add_steps_to_day":
                pass
            case "palindrome":
                pass
            case "steps_of_consecutive_digits":
                pass
            case "steps_multiple_number":
                pass
            case "add_steps_to_report_digit":
                pass
            case "best_personal_record":
                pass
            case _:
                return None
