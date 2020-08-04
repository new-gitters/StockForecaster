from django.db import models

# Create your models here.
class HistoricalData(models.Model):
    symbol = models.CharField(max_length=50)
    time = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

class RealTimeData(models.Model):
    symbol = models.CharField(max_length=50)
    time = models.DateField()
    price = models.FloatField()
    volume = models.IntegerField()