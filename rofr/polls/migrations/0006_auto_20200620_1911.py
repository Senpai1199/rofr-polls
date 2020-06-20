# Generated by Django 3.0.7 on 2020-06-20 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200620_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='max_age',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='max_income',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='min_age',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poll',
            name='min_income',
            field=models.SmallIntegerField(default=0),
        ),
    ]
