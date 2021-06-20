from django.db import models

# Create your models here.


class Game(models.Model):
    title = models.CharField(default="untitled", max_length=200)
    description = models.CharField(default="untitled", max_length=500)
    move_list = models.CharField(default="", max_length=2000)
    white = models.CharField(default="stockfish", max_length=200)
    white_level = models.IntegerField(default=1)
    black = models.CharField(default="stockfish", max_length=200)
    black_level = models.IntegerField(default=1)
    time_controls = models.IntegerField(default=100)
    class Meta:
        ordering = ['title']