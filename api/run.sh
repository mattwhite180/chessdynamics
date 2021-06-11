#!/bin/bash

docker build -t chessdynamics . && docker run -it chessdynamics $1 $2 $3 $4 $5 $6
