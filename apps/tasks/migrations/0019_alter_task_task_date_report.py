# Generated by Django 4.0.10 on 2023-12-26 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_alter_task_task_date_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_date_report',
            field=models.DateField(blank=True, default=datetime.date(2023, 12, 25), null=True, verbose_name='День с какого берем шаги (D)'),
        ),
    ]