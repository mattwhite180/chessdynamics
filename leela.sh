docker-compose down --remove-orphans && \
docker-compose build \
&& docker-compose run api ipython3 manage.py testleela
