# Generated by Django 4.0.10 on 2023-12-14 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0007_step_karathon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Задание дня выполнено'),
        ),
    ]