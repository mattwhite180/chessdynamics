# base image
FROM node:14 AS basedependenciesfront
ENV TZ="America/Denver"

# set working directory
WORKDIR /app

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
	vim \
	git \
    && rm -rf /var/lib/apt/lists/*

# add `/app/node_modules/.bin` to $PATH
#ENV PATH /app/node_modules/.bin:$PATH

RUN git clone https://github.com/jhlywa/chess.js

# install and cache app dependencies

COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@7.3.9
RUN npm install chessboardjs --save
RUN npm install jquery --save

FROM basedependenciesfront AS front
# add app
COPY . .
RUN ng build

# start app
#CMD ng serve --host 0.0.0.0
CMD echo 'done building front end'