docker-compose down --remove-orphans && docker-compose build && docker-compose run api python3 manage.py test
