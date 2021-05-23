from django.db import models

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    PGN = models.CharField(max_length=20000)
    black = models.CharField(max_length=200)
    black_level = models.IntegerField()
    white= models.CharField(max_length=200)
    white_level = models.IntegerField()
    time_controls = models.FloatField()
