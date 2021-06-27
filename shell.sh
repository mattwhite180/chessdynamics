docker-compose down --remove-orphans && \
	docker-compose build && \
	docker-compose run api bash -c "python3 manage.py makemigrations && python3 manage.py migrate"
	echo "from chessapp.models import Game"
	echo "from chessapp.chessdynamics import GameModel"
	echo "from django.contrib.auth.models import User"
	echo 'u = User.objects.get(username="test1")'
	echo 'g = Game.objects.get(title="random")'
	echo 'gm = GameModel(g)'
	echo 'gm.play_continuous()'
	docker-compose run api bash -c "python3 manage.py shell"
