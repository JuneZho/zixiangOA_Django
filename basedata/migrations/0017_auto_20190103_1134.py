# Generated by Django 2.0.7 on 2019-01-03 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0016_device_changelog_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=7, max_length=8, null=True, verbose_name='总金额')),
                ('agreed', models.BooleanField(default=False, verbose_name='已同意')),
                ('workflow_node', models.IntegerField(choices=[(0, '等待'), (1, '库管'), (2, '完成')], default=0, verbose_name='工作流节点')),
                ('project_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '材料领用',
                'verbose_name_plural': '材料领用',
            },
        ),
        migrations.CreateModel(
            name='work_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='月份')),
                ('input_date', models.DateField(auto_now_add=True, null=True, verbose_name='填写日期')),
                ('agreed', models.BooleanField(default=False, verbose_name='已同意')),
                ('workflow_node', models.IntegerField(choices=[(0, '等待'), (1, '工程经理'), (2, '技术经理'), (3, '行政经理'), (4, '完成')], default=0, verbose_name='工作流节点')),
                ('project_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Project', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '工时记录',
                'verbose_name_plural': '工时记录',
            },
        ),
        migrations.AlterModelOptions(
            name='material_use',
            options={'verbose_name': '材料领单项', 'verbose_name_plural': '材料领用单项'},
        ),
        migrations.AlterModelOptions(
            name='work_hour',
            options={'verbose_name': '工时记录单项', 'verbose_name_plural': '工时记录单项'},
        ),
        migrations.RemoveField(
            model_name='material_use',
            name='project_info',
        ),
        migrations.RemoveField(
            model_name='work_hour',
            name='agreed',
        ),
        migrations.RemoveField(
            model_name='work_hour',
            name='project_info',
        ),
        migrations.RemoveField(
            model_name='work_hour',
            name='workflow_node',
        ),
        migrations.AddField(
            model_name='material_use',
            name='material_log',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Material_log', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='work_hour',
            name='work_report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.work_report', verbose_name='所属项目'),
        ),
    ]
