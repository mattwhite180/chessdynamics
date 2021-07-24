FROM python:3.10.0b3-buster AS basedependencies
ENV TZ="America/Denver"

EXPOSE 8000

WORKDIR /root/

RUN apt-get update -y \                                                                                        
    && apt-get install -y \                                                                                    
    	ipython3 \
	python3-pip \
	stockfish \
	vim \
	postgresql \
	build-essential \
	procps \
	curl \
	file \
	git \
	sudo \
    libopenblas-dev \
    ninja-build \
    libgtest-dev \
    libstdc++-8-dev \
    clang-6.0 \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

##############
# leela lc0
FROM basedependencies AS leela
RUN git clone -b release/0.27 https://github.com/LeelaChessZero/lc0
WORKDIR /root/lc0/
RUN bash build.sh
WORKDIR /root/lc0/build/release/
COPY weights_run2_744679.pb.gz .
########

FROM leela
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY chesssite .


#RUN python3 manage.py makemigrations

#RUN python3 manage.py migrate

CMD echo "done building api"
#CMD bash -c "hostname -I && python3 manage.py runserver 0:8000"
