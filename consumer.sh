#!/bin/bash
for (( i=1; i<=$1; i++ ))
do
    echo "docker exec chessdynamics_api_$i python3 manage.py testapi &"
    docker exec chessdynamics_api_$i python3 manage.py testapi &
done