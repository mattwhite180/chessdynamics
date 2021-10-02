# base image
FROM node:14
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

COPY package.json package.json
RUN npm install
RUN npm install --save-dev @angular-devkit/build-angular
RUN npm install --save @angular-devkit/build-angular
RUN npm install -g @angular/cli@latest
RUN npm install chessboardjs --save
RUN npm install jquery --save


# add app

# COPY . .
# RUN ng build

# start app
# CMD ng serve --host 0.0.0.0
CMD echo 'done building front end'
