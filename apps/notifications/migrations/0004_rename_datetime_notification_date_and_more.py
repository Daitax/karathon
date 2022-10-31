# Generated by Django 4.1 on 2022-10-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_notificationtemplate_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='datetime',
            new_name='date',
        ),
        migrations.AlterField(
            model_name='notification',
            name='header',
            field=models.CharField(max_length=100, verbose_name='Вставка в заголовок'),
        ),
        migrations.AlterField(
            model_name='notificationtemplate',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Название'),
        ),
    ]
