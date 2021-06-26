# Generated by Django 2.1.15 on 2021-06-22 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('activity', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'chatmetric',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ErrorMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('error', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'errormetric',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SensorMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('temperature', models.IntegerField()),
                ('humidity', models.IntegerField()),
                ('luminosity', models.IntegerField()),
            ],
            options={
                'db_table': 'sensormetric',
                'managed': False,
            },
        ),
    ]