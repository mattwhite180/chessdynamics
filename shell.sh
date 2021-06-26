docker-compose down --remove-orphans && \
	docker-compose build && \
	echo "from chessapp.models import Game"
	echo "from chessapp.chessdynamics import GameModel"
	echo "from django.contrib.auth.models import User"
	docker-compose run api bash -c "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py shell"
