# Generated by Django 2.0.7 on 2018-10-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_merge_20180829_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='selleruser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
