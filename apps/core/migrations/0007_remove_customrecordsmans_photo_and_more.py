# Generated by Django 4.0.10 on 2023-12-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_customrecordsmans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customrecordsmans',
            name='photo',
        ),
        migrations.AddField(
            model_name='customrecordsmans',
            name='participant_photo',
            field=models.ImageField(default=1, upload_to='recordsmans', verbose_name='Фото рекордсмена'),
            preserve_default=False,
        ),
    ]
