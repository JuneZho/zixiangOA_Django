# Generated by Django 2.0.7 on 2019-01-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0042_auto_20190107_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback_form',
            name='bonus',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, max_length=8, null=True, verbose_name='项目经理奖励金额'),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_mat',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='材料金额'),
        ),
        migrations.AlterField(
            model_name='project',
            name='workflow_node',
            field=models.IntegerField(choices=[(0, '等待填写人发起'), (1, '营销经理'), (2, '商务经理'), (3, '技术中心经理'), (4, '财务经理'), (5, '总经理'), (6, '工程经理'), (7, '普通员工'), (8, '技术经理'), (9, '行政经理'), (10, '总经理'), (12, '完成')], default=0, verbose_name='工作流节点'),
        ),
    ]