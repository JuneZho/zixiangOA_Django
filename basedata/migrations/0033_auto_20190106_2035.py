# Generated by Django 2.0.7 on 2019-01-06 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basedata', '0032_auto_20190106_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device_final',
            name='project_info',
        ),
        migrations.RemoveField(
            model_name='device_final',
            name='workflow_node',
        ),
    ]
