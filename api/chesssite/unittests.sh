echo 'sleeping for 10'
sleep 10
echo 'done sleeping'
python3 manage.py makemigrations && \
python3 manage.py migrate && \
python3 manage.py test
