# Generated by Django 2.0.7 on 2019-01-17 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0068_auto_20190117_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_final',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, max_length=8, null=True, verbose_name='单价'),
        ),
    ]
