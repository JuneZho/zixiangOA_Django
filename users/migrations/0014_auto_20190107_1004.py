# Generated by Django 2.0.7 on 2019-01-07 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_employee_recent_pro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='title',
            field=models.IntegerField(blank=True, choices=[(0, '普通员工'), (1, '总经理'), (2, '商务经理'), (3, '财务经理'), (4, '工程经理'), (5, '技术经理'), (6, '库管'), (7, '营销经理'), (8, '行政经理'), (9, '技术经理')], default=0, null=True, verbose_name='权限'),
        ),
    ]