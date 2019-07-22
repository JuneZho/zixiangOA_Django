# Generated by Django 2.0.7 on 2019-01-06 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0034_auto_20190106_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_change',
            name='brand',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='品牌'),
        ),
        migrations.AlterField(
            model_name='device_change',
            name='reason',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='变更原因'),
        ),
        migrations.AlterField(
            model_name='device_change',
            name='specification',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='规格'),
        ),
        migrations.AlterField(
            model_name='material_use',
            name='brand',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='品牌'),
        ),
        migrations.AlterField(
            model_name='project',
            name='contract',
            field=models.CharField(blank=True, default='', max_length=40, verbose_name='合同编号'),
        ),
    ]
