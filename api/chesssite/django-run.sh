#!/bin/bash

FILE=djangosecret.txt

if [ -f "$FILE" ]; then
    echo "djangosecret.txt exists."
else 
    echo "$FILE does not exist."
    python3 create-secret.py > $FILE
    echo "created $FILE"
fi

python3 manage.py makemigrations chessapp && \
python3 manage.py makemigrations && \
python3 manage.py migrate && \
python3 manage.py runserver 0:8000