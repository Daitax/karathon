# Generated by Django 4.0.10 on 2023-10-31 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_participant_timezone_offset'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sms',
            new_name='EmailCode',
        ),
    ]