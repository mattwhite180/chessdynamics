FROM python:3.10.0b3-buster AS basedependencies
ENV TZ="America/Denver"

EXPOSE 5000

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
    	ipython3 \
	python3-pip \
    && rm -rf /var/lib/apt/lists/*

FROM basedependencies
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY script.py .

#RUN python3 manage.py makemigrations

#RUN python3 manage.py migrate

CMD echo "done building consumer"
#CMD bash -c "hostname -I && python3 manage.py runserver 0:8000"
