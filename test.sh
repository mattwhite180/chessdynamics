docker-compose down --remove-orphans && \
docker-compose build && \
docker-compose run api bash -c \
"sleep 10 && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py test" && \
docker-compose down --remove-orphans
