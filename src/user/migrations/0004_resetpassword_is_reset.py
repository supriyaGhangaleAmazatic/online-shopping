# Generated by Django 2.0.7 on 2018-08-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20180820_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='resetpassword',
            name='is_reset',
            field=models.BooleanField(default=False),
        ),
    ]
