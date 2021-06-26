from django.db import models

# Create your models here.


class Game(models.Model):
    title = models.CharField(default="untitled", blank=True, max_length=200)
    description = models.CharField(default="untitled", blank=True, max_length=500)
    move_list = models.CharField(default="", blank=True, max_length=2000)
    white = models.CharField(default="stockfish", blank=True, max_length=200)
    white_level = models.IntegerField(default=1, blank=True)
    black = models.CharField(default="stockfish", blank=True, max_length=200)
    black_level = models.IntegerField(default=1, blank=True)
    time_controls = models.IntegerField(default=100, blank=True)
    results = models.CharField(default="...", blank=True, max_length=10)
    fen = models.CharField(default="", blank=True, max_length=200)
    legal_moves = models.CharField(default="", blank=True, max_length=2000)
    owner = models.ForeignKey(
        "auth.User", related_name="games", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["title"]
