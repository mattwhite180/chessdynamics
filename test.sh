docker-compose down --remove-orphans && \
docker-compose build && \
docker-compose run api bash -c \
"sleep 10 && python3 manage.py makemigrations chessapp && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py test $1 $2 $3" && \
docker-compose down --remove-orphans
