# Generated by Django 2.0.7 on 2019-01-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20180810_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='recent_pro',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='最近访问'),
        ),
    ]
