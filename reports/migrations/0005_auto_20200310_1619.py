# Generated by Django 2.2.10 on 2020-03-10 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20200304_0252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-date'], 'verbose_name': 'Отчет', 'verbose_name_plural': 'Отчеты'},
        ),
    ]