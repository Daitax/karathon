# Generated by Django 4.0.10 on 2023-11-03 09:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_individualtask_task_date_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualtask',
            name='task_date_report',
            field=models.DateField(blank=True, default=datetime.date(2023, 11, 2), null=True, verbose_name='День с какого берем шаги (D)'),
        ),
    ]