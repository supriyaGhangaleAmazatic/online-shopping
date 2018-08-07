# Generated by Django 2.0.7 on 2018-08-07 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='user',
            name='user_index',
        ),
        migrations.AlterField(
            model_name='role',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name', 'last_name', 'gender', 'dob'], name='user_index'),
        ),
    ]
