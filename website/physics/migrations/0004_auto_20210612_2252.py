# Generated by Django 2.1.15 on 2021-06-12 22:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('physics', '0003_auto_20210612_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date published'),
        ),
    ]
