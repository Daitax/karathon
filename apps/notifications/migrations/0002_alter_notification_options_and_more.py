# Generated by Django 4.1 on 2022-10-21 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={},
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='client',
            new_name='participant',
        ),
    ]