FROM debian:buster

EXPOSE 8000

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
    	ipython3 \
	python3-pip \
	stockfish \
	vim \
	postgresql \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY chesssite .


#RUN python3 manage.py makemigrations

#RUN python3 manage.py migrate

CMD echo "done building api"
#CMD bash -c "hostname -I && python3 manage.py runserver 0:8000"
