# Generated by Django 3.0.7 on 2020-06-22 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='poll',
        ),
        migrations.AddField(
            model_name='userresponse',
            name='poll',
            field=models.ManyToManyField(null=True, related_name='responses', to='polls.Poll'),
        ),
    ]
