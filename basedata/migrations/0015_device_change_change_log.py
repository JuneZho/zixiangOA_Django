# Generated by Django 2.0.7 on 2019-01-01 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0014_auto_20190101_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_change',
            name='change_log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Device_changelog', verbose_name='修改次数'),
        ),
    ]
