#!/bin/bash

docker build -t flasktest . && docker run -it flasktest $1 $2 $3 $4 $5 $6
