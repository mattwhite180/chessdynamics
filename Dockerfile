FROM debian:buster

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
    	ipython3 \
	python3-pip \
	stockfish \
	vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

CMD python3 chessdynamics.py
