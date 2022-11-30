# Generated by Django 4.1 on 2022-10-28 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamparticipant',
            options={'verbose_name': 'Участник команды', 'verbose_name_plural': 'Участники команды'},
        ),
        migrations.CreateModel(
            name='DesiredTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desired_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desired', to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]