# Generated by Django 2.2.12 on 2020-04-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nav_client', '0010_auto_20200420_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geozone',
            name='nav_id',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='nav_id'),
        ),
    ]
