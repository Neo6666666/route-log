# Generated by Django 2.2.10 on 2020-03-11 03:18

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nav_client', '0004_geozone_mt_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syncdate',
            name='datetime',
            field=models.DateTimeField(
                default=timezone.localtime, verbose_name='Дата синхронизации'),
        ),
    ]
