from django.db import models
class DriverState(models.Model):
    Modes = [
        ('Idle','idle'),
        ('Engaged','engaged'),
        ('Offline','offline')
    ]
    driver_id = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    state = models.CharField(max_length=7,choices=Modes,default='offline')