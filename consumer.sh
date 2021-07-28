#!/bin/bash
count=$(docker ps 2> /dev/null | grep api | wc | awk '{print $1}')
for (( i=1; i<$count; i++ ))
do
    echo "docker exec chessdynamics_api_$i python3 manage.py testapi &"
    docker exec chessdynamics_api_$i python3 manage.py consumer $1 $2 &
done
