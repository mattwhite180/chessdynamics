FROM debian:buster

EXPOSE 5000

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
	vim \
	npm \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN npm install --save react-chessground

RUN npm run build

RUN npm install -g serve
#RUN python3 manage.py makemigrations

#RUN python3 manage.py migrate

CMD echo 'done building fronend'
#CMD bash -c "hostname -I && python3 manage.py runserver 0:8000"
