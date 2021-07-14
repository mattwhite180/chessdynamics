#!/bin/bash
if [ -z "$1" ]; then
        APICOUNT="1"
else
        APICOUNT=$1
fi


docker-compose down --remove-orphans && \
docker-compose build \
&& docker-compose up --scale api=$APICOUNT
