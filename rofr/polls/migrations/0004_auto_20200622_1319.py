# Generated by Django 3.0.7 on 2020-06-22 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200622_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='poll',
        ),
        migrations.AddField(
            model_name='userresponse',
            name='poll',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='polls.Poll'),
            preserve_default=False,
        ),
    ]
