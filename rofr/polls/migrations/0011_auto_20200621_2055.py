# Generated by Django 3.0.7 on 2020-06-21 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0010_auto_20200621_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='poll_taker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
