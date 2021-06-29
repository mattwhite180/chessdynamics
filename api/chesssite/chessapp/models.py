from django.db import models

# Create your models here.


class Game(models.Model):
    name = models.CharField(default="untitled", blank=True, max_length=200)
    description = models.CharField(default="untitled", blank=True, max_length=500)
    move_list = models.CharField(default="", blank=True, max_length=2000)
    white = models.CharField(default="stockfish", blank=True, max_length=200)
    white_level = models.IntegerField(default=1, blank=True)
    black = models.CharField(default="stockfish", blank=True, max_length=200)
    black_level = models.IntegerField(default=1, blank=True)
    time_controls = models.IntegerField(default=100, blank=True)
    results = models.CharField(default="*", blank=True, max_length=10)
    fen = models.CharField(default="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", blank=True, max_length=200)
    legal_moves = models.CharField(default='g1h3,g1f3,b1c3,b1a3,h2h3,g2g3,f2f3,e2e3,d2d3,c2c3,b2b3,a2a3,h2h4,g2g4,f2f4,e2e4,d2d4,c2c4,b2b4,a2a4', blank=True, max_length=2000)
    owner = models.ForeignKey(
        "auth.User", related_name="games", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["name"]
