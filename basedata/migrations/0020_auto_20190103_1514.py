# Generated by Django 2.0.7 on 2019-01-03 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0019_material_log_thisid'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contract',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='合同编号'),
        ),
        migrations.AlterField(
            model_name='project',
            name='payertele',
            field=models.CharField(default='无', max_length=20, verbose_name='付款电话'),
        ),
    ]
