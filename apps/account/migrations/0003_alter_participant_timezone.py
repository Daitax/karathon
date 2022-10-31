# Generated by Django 4.1 on 2022-10-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_participant_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='timezone',
            field=models.CharField(choices=[('Europe/Moscow', 'Мск'), ('Europe/Samara', 'Мск+01'), ('Asia/Yekaterinburg', 'Мск+02'), ('Asia/Omsk', 'Мск+03'), ('Asia/Novosibirsk', 'Мск+04'), ('Asia/Irkutsk', 'Мск+05'), ('Asia/Yakutsk', 'Мск+06'), ('Asia/Vladivostok', 'Мск+07'), ('Asia/Sakhalin', 'Мск+08'), ('Asia/Kamchatka', 'Мск+09'), ('Europe/Kaliningrad', 'Мск-01'), ('Europe/London', 'Мск-02'), ('UTC', 'Мск-03'), ('Atlantic/Cape_Verde', 'Мск-04'), ('Atlantic/South_Georgia', 'Мск-05'), ('America/Buenos_Aires', 'Мск-06'), ('America/New_York', 'Мск-07'), ('America/Panama', 'Мск-08'), ('America/Edmonton', 'Мск-09'), ('America/Los_Angeles', 'Мск-10'), ('America/Anchorage', 'Мск-11'), ('America/Adak', 'Мск-12'), ('Pacific/Honolulu', 'Мск-13'), ('Pacific/Midway', 'Мск-14')], default='Europe/Moscow', max_length=30),
        ),
    ]
