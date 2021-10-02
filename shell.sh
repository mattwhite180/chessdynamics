echo 'from chessapp.models import Game'
echo 'from chessapp.chessdynamics import GameHandler, Stockfish, Leela, RandomEngine'
echo ''
docker exec -it chessdynamics_api_1 python3 manage.py shell
