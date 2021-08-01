#!/bin/bash

docker build -t flasktest . && docker run -it -v ~/.aws:/root/.aws flasktest $1 $2 $3 $4 $5 $6
