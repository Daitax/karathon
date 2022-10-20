# Generated by Django 4.1 on 2022-10-20 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_task_addition_alter_task_category_and_more'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
    ]
