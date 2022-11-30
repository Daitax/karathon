# Generated by Django 4.1 on 2022-11-23 10:10

import apps.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[apps.core.validators.not_earlier_today], verbose_name='Дата')),
                ('type', models.CharField(choices=[('walk_steps', 'Пройти S шагов'), ('double_best', 'Удвоить лучший результат или S шагов'), ('double_result_day', 'Удвоить результат дня D или S шагов'), ('improve_best', 'Улучшить лучший результат или S шагов'), ('improve_result_day', 'Улучшить результат дня D или S шагов'), ('add_steps_to_day', 'Добавить S шагов ко дню D'), ('palindrome', 'Зеркалка'), ('steps_of_consecutive_digits', 'Число шагов из последовательных цифр'), ('steps_multiple_number', 'Число шагов, кратное N'), ('add_steps_to_report_digit', 'Добавить X-тысяч шагов, где X - цифра в отчёте дня D, занимающая позицию P'), ('beat_personal_record', 'Побить личный рекорд или S шагов')], max_length=100, verbose_name='Тип')),
                ('steps', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество шагов в задании (S)')),
                ('task_date_report', models.DateField(blank=True, null=True, verbose_name='День с какого берем шаги (D)')),
                ('multiple_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Кол-во шагов, кратное этому числу (N)')),
                ('position', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Позиция цифры в отчёте (P)')),
                ('task', models.CharField(max_length=200, verbose_name='Задание')),
                ('addition', models.CharField(blank=True, max_length=200, null=True, verbose_name='Дополнение к заданию')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
                ('karathon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.karathon')),
            ],
            options={
                'verbose_name': 'Индивидуальное задание',
                'verbose_name_plural': 'Индивидуальные задания',
            },
        ),
    ]