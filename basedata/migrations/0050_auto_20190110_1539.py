# Generated by Django 2.0.7 on 2019-01-10 15:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0049_auto_20190110_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_change',
            name='unit',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='单位'),
        ),
        migrations.AlterField(
            model_name='device_changelog',
            name='thisid',
            field=models.IntegerField(default=1, verbose_name='变更次数'),
        ),
        migrations.AlterField(
            model_name='outsource_items',
            name='num',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5000), django.core.validators.MinValueValidator(0)], verbose_name='外包数量'),
        ),
        migrations.AlterField(
            model_name='outsource_items',
            name='provider',
            field=models.CharField(blank=True, default='', max_length=8, null=True, verbose_name='外包施工负责人'),
        ),
        migrations.AlterField(
            model_name='outsource_items',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, max_length=8, null=True, verbose_name='金额'),
        ),
        migrations.AlterField(
            model_name='work_hour',
            name='extra_work_hour',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=4, max_length=8, null=True, verbose_name='上班工时/单价100'),
        ),
        migrations.AlterField(
            model_name='work_hour',
            name='finish_time',
            field=models.DateField(blank=True, null=True, verbose_name='结束日期'),
        ),
        migrations.AlterField(
            model_name='work_hour',
            name='inside_work_hour',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=4, max_length=8, null=True, verbose_name='工时费'),
        ),
        migrations.AlterField(
            model_name='work_hour',
            name='start_time',
            field=models.DateField(blank=True, null=True, verbose_name='开始日期'),
        ),
        migrations.AlterField(
            model_name='work_hour',
            name='work_content',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='工作内容'),
        ),
    ]