import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from apps.account.models import Participant
from apps.core.models import Category, Karathon
from apps.core.utils import ending_numbers, format_date
from apps.core.validators import not_earlier_today


class Task(models.Model):
    TYPE = (
        ("walk_steps", "Пройти S шагов"),
        ("double_best", "Удвоить лучший результат или S шагов"),
        ("double_result_day", "Удвоить результат дня D или S шагов"),
        ("improve_best", "Улучшить лучший результат или S шагов"),
        ("improve_result_day", "Улучшить результат дня D или S шагов"),
        ("add_steps_to_day", "Добавить S шагов ко дню D"),
        ("palindrome", "Зеркалка, но не менее S шагов"),
        ("steps_of_consecutive_digits", "Число шагов из последовательных цифр"),
        ("steps_multiple_number", "Число шагов, кратное N, но не менее S шагов"),
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
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return "Задание для {category} на {date}".format(category=self.category, date=format_date(self.date))

    def text_task(self, participant):
        match self.type:
            case "walk_steps":
                text = "Пройди {} {}".format(
                    self.steps,
                    ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                )

            case "double_best":
                best_steps = participant.best_steps_karathon()

                if best_steps:
                    text = "Удвой свой лучший результат ({} {}) или пройди не менее {} {}".format(
                        best_steps,
                        ending_numbers(best_steps, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов']),
                    )
                else:
                    text = "Пройди не менее {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "double_result_day":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)

                    text = "Удвой результат дня за {} ({} {}) или пройди не менее {} {}".format(
                        format_date(self.task_date_report),
                        day_steps.steps,
                        ending_numbers(day_steps.steps, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов']),
                    )

                except ObjectDoesNotExist:
                    text = "Пройди не менее {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "improve_best":
                best_steps = participant.best_steps_karathon()

                if best_steps:
                    text = "Улучши свой лучший результат ({} {}) или пройди не менее {} {}".format(
                        best_steps,
                        ending_numbers(best_steps, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов']),
                    )
                else:
                    text = "Пройди не менее {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "improve_result_day":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)
                    steps = day_steps.steps

                    text = "Улучши результат дня за {} ({} {}) или пройди не менее {} {}".format(
                        format_date(self.task_date_report),
                        day_steps.steps,
                        ending_numbers(day_steps.steps, ['шаг', 'шага', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов']),
                    )

                except ObjectDoesNotExist:
                    text = "Пройди не менее {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "add_steps_to_day":
                from apps.steps.models import Step
                try:
                    day_steps = Step.objects.get(participant=participant, date=self.task_date_report)
                    steps = day_steps.steps

                    text = "Добавь {} {} к шагам {} ({} {})".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов']),
                        format_date(self.task_date_report),
                        day_steps.steps,
                        ending_numbers(steps + self.steps, ['шаг', 'шага', 'шагов']),
                    )
                except ObjectDoesNotExist:
                    steps = 0

                    text = "Пройди не менее {} {}".format(
                        steps + self.steps,
                        ending_numbers(steps + self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case "palindrome":
                text = "Пройди зеркальное количество шагов (например 12321), но не менее {} {}".format(
                    self.steps,
                    ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                )

            case "steps_of_consecutive_digits":
                text = "Пройди количество шагов, состоящее из последовательных цифр (например 12543)"

            case "steps_multiple_number":
                text = "Пройди число шагов, кратное {}, но не менее {} {}".format(
                    self.multiple_number,
                    self.steps,
                    ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                )

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

                text = "Пройди не менее {} {}".format(
                    steps,
                    ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                )

            case "best_personal_record":
                best_steps = participant.best_steps_all()

                if best_steps:
                    text = "Побей свой личный рекорд ({} {}) или пройди больше {} {}".format(
                        best_steps,
                        ending_numbers(best_steps, ['шага', 'шагов', 'шагов']),
                        self.steps,
                        ending_numbers(self.steps, ['шага', 'шагов', 'шагов']),
                    )
                else:
                    text = "Пройди больше {} {}".format(
                        self.steps,
                        ending_numbers(self.steps, ['шаг', 'шага', 'шагов'])
                    )

            case _:
                return None

        return text

    @staticmethod
    def is_task_completed(report):
        task = report.participant.task_of_day(report.date)

        if task:
            from apps.steps.models import Step

            match task.type:
                case "walk_steps":
                    if task.steps <= report.steps:
                        return True

                case "double_best":
                    karathon = report.participant.get_active_karathon()

                    best_steps = Step.objects.filter(
                        participant=report.participant,
                        karathon=karathon
                    ).exclude(date=report.date).order_by('-steps').first()
                    if best_steps:
                        steps = best_steps.steps * 2
                    else:
                        steps = 0

                    total_steps = min(steps, task.steps)

                    if total_steps <= report.steps:
                        return True

                case "double_result_day":
                    try:
                        day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)

                        steps = day_steps.steps * 2
                    except ObjectDoesNotExist:
                        steps = 0

                    total_steps = min(steps, task.steps)

                    if total_steps <= report.steps:
                        return True

                case "improve_best":
                    karathon = report.participant.get_active_karathon()

                    best_steps = Step.objects.filter(
                        participant=report.participant,
                        karathon=karathon
                    ).exclude(date=report.date).order_by('-steps').first()
                    if best_steps:
                        steps = best_steps.steps
                    else:
                        steps = 0

                    total_steps = min(steps, task.steps)

                    if total_steps < report.steps:
                        return True

                case "improve_result_day":
                    try:
                        day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)
                        steps = day_steps.steps
                    except ObjectDoesNotExist:
                        steps = 0

                    total_steps = min(steps, task.steps)

                    if total_steps < report.steps:
                        return True

                case "add_steps_to_day":
                    try:
                        day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)
                        steps = day_steps.steps
                    except ObjectDoesNotExist:
                        steps = 0

                    if steps + task.steps <= report.steps:
                        return True

                case "palindrome":
                    copy_report_steps = report.steps
                    result_number = 0

                    while copy_report_steps != 0:
                        digit = copy_report_steps % 10
                        result_number = result_number * 10 + digit
                        copy_report_steps = int(copy_report_steps / 10)

                    if result_number == report.steps and task.steps < report.steps:
                        return True

                case "steps_of_consecutive_digits":
                    digit_list = sorted([int(a) for a in str(report.steps)])
                    for i in range(len(digit_list) - 1):
                        if digit_list[i] + 1 == digit_list[i + 1]:
                            pass
                        else:
                            return False
                    return True

                case "steps_multiple_number":
                    if report.steps % task.multiple_number == 0 and task.steps < report.steps:
                        return True

                case "add_steps_to_report_digit":
                    try:
                        day_steps = Step.objects.get(participant=report.participant, date=task.task_date_report)
                        digit_list = [int(a) for a in str(day_steps.steps)]

                        if task.position > len(digit_list):
                            position = task.position % len(digit_list)
                        else:
                            position = task.position

                        digit = int(digit_list[position - 1])
                        digit = 5 if digit == 0 else digit
                    except ObjectDoesNotExist:
                        digit = 5

                    steps = digit * 1000

                    if steps <= report.steps:
                        return True

                case "best_personal_record":
                    best_steps = Step.objects.filter(
                        participant=report.participant
                    ).exclude(date=report.date).order_by('-steps').first()

                    if best_steps:
                        steps = best_steps.steps
                    else:
                        steps = 0

                    total_steps = min(steps, task.steps)

                    if total_steps < report.steps:
                        return True

        return False
