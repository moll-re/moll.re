# Generated by Django 2.1.15 on 2021-06-12 22:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('physics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default='No content yet'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 12, 22, 50, 36, 599931), verbose_name='Date published'),
        ),
        migrations.AddField(
            model_name='posttopic',
            name='Post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='physics.Post'),
        ),
    ]