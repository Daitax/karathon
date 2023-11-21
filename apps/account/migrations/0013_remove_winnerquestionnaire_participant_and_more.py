# Generated by Django 4.0.10 on 2023-11-20 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_rename_сharity_сategory_winnerquestionnaire_charity_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winnerquestionnaire',
            name='participant',
        ),
        migrations.AddField(
            model_name='winnerquestionnaire',
            name='winner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.winner', verbose_name='Победитель'),
            preserve_default=False,
        ),
    ]
