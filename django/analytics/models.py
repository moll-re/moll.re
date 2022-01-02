from django.db import models
import json

class ChatMetric(models.Model):
    time = models.DateTimeField()
    send = models.BooleanField()
    read = models.BooleanField()
    execute = models.BooleanField()


    class Meta:
        managed = False
        db_table = 'chatmetric'


class ErrorMetric(models.Model):
    time = models.DateTimeField()
    error = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'errormetric'


class SensorMetric(models.Model):
    time = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    luminosity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'sensormetric'


class AIOList(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()

    @property
    def content_as_list(self):
        return json.loads(self.content or "[]")

    class Meta:
        managed = False
        db_table = 'list'