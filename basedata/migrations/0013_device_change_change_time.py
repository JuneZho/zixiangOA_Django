# Generated by Django 2.0.7 on 2019-01-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0012_auto_20180829_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_change',
            name='change_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='修改次数'),
        ),
    ]
