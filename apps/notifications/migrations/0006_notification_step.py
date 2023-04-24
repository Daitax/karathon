# Generated by Django 4.1 on 2023-04-24 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('steps', '0005_step_bonus_step_is_completed'),
        ('notifications', '0005_alter_notification_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='step',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='steps.step'),
        ),
    ]
