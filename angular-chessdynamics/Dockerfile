# base image
FROM node:14
ENV TZ="America/Denver"

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
#ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@7.3.9
RUN npm install chessground

# add app
COPY . /app
RUN ng build

# start app
#CMD ng serve --host 0.0.0.0
CMD echo 'done building front end'