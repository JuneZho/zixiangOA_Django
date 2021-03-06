# Generated by Django 2.0.7 on 2019-01-17 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0066_auto_20190117_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='buy_from',
            field=models.TextField(blank=True, null=True, verbose_name='供应商'),
        ),
        migrations.AlterField(
            model_name='device_change',
            name='name',
            field=models.TextField(blank=True, default='', null=True, verbose_name='设备名称'),
        ),
        migrations.AlterField(
            model_name='device_change',
            name='specification',
            field=models.TextField(blank=True, null=True, verbose_name='规格'),
        ),
    ]
