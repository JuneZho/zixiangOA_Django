# Generated by Django 2.0.7 on 2019-01-04 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0026_auto_20190104_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_form',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Device_form', verbose_name='表单'),
        ),
        migrations.AlterField(
            model_name='device',
            name='project_info',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='basedata.Project', verbose_name='所属项目'),
        ),
    ]
