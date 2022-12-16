import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from apps.account.models import Participant
from apps.core.models import Category, Karathon
from apps.core.utils import ending_numbers
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
                text = "Пройдите {} {}".format(
                    self.steps,
                    ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                )

            case "double_best":
                best_steps = participant.best_steps_karathon()

                if best_steps:
                    double_best = best_steps * 2

                    text = "Пройдите {} {} или {} {}".format(
                        double_best,
                        ending_numbers(double_best, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )
                else:
                    text = "Пройдите {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "double_result_day":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)
                    double_steps = day_steps.steps * 2

                    text = "Пройдите {} {} или {} {}".format(
                        double_steps,
                        ending_numbers(double_steps, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

                except ObjectDoesNotExist:
                    text = "Пройдите {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "improve_best":
                best_steps = participant.best_steps_karathon()

                if best_steps:
                    text = "Пройдите больше {} {} или {} {}".format(
                        best_steps,
                        ending_numbers(best_steps, ['шага', 'шагов', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )
                else:
                    text = "Пройдите {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "improve_result_day":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)
                    steps = day_steps.steps

                    text = "Пройдите больше {} {} или {} {}".format(
                        steps,
                        ending_numbers(steps, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

                except ObjectDoesNotExist:
                    text = "Пройдите {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "add_steps_to_day":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)
                    steps = day_steps.steps
                except ObjectDoesNotExist:
                    steps = 0

                text = "Пройдите {} {}".format(
                    steps + self.steps,
                    ending_numbers(steps + self.steps, ['шаг', 'шага', 'шагов'])
                )

            case "palindrome":
                text = "Пройдите зеркальное количество шагов (например 12321)"

            case "steps_of_consecutive_digits":
                text = "Пройдите количество шагов, состоящее из последовательных цифр (например 12543)"

            case "steps_multiple_number":
                text = "Пройдите число шагов, кратное {}".format(self.multiple_number)

            case "add_steps_to_report_digit":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)

                    digit_list = [int(a) for a in str(day_steps.steps)]

                    if self.position > len(digit_list):
                        position = self.position % len(digit_list)
                    else:
                        position = self.position

                    digit = int(digit_list[position - 1])
                    digit = 5 if digit == 0 else digit
                except ObjectDoesNotExist:
                    digit = 5

                steps = digit * 1000

                text = "Пройдите {} {}".format(
                    steps,
                    ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                )

            case "best_personal_record":
                best_steps = participant.best_steps_all()

                if best_steps:
                    text = "Пройдите больше {} {} или {} {}".format(
                        best_steps,
                        ending_numbers(best_steps, ['шага', 'шагов', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )
                else:
                    text = "Пройдите {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case _:
                return None

        return text
