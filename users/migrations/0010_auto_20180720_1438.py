# Generated by Django 2.0.7 on 2018-07-20 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20180720_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateField(auto_now=True),
        ),
    ]
