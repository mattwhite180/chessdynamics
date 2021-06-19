from django.db import models

# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    move_list = models.CharField(max_length=2000)
    black = models.CharField(max_length=200)
    black_level = models.IntegerField()
    white = models.CharField(max_length=200)
    white_level = models.IntegerField()
    time_controls = models.FloatField()
