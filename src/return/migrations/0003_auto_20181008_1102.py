# Generated by Django 2.0.7 on 2018-10-08 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('return', '0002_auto_20180925_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='lineitem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.Lineitem'),
        ),
    ]
