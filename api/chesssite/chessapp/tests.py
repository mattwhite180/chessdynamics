from django.test import TestCase
from .models import Game
from .chessdynamics import ChessPlayer, ChessGame, GameModel 


class ChessPlayerTestCase(TestCase):
    def setup(self):
        pass
    
    def test_time(self):
        c = ChessPlayer("test_time", 123)
        val = c.get_time_limit()
        expected = 123 / 1000
        errmsg = (
            "expected value is " + str(expected) +
            "actual value is " + str(val)
        )
        self.assertEqual(val, expected, errmsg)

    def test_cpu_name(self):
        c = ChessPlayer("stockfish", 123)
        val = c.is_cpu()
        expected = True
        errmsg = (
            "expected value is " + str(expected) +
            "actual value is " + str(val)
        )
        self.assertEqual(val, expected, errmsg) 

    def test_human_name(self):
        c = ChessPlayer("matthew", 123)
        val = c.is_cpu()
        expected = False
        errmsg = (
            "expected value is " + str(expected) +
            "actual value is " + str(val)
        )
        self.assertEqual(val, expected, errmsg) 
# Create your tests here.
#Class BongCloudTestCase(TestCase):
