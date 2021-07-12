FROM python:3.10.0b3-buster AS basedependencies
ENV TZ="America/Denver"

EXPOSE 8000

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
    && rm -rf /var/lib/apt/lists/*

##############
# leela lc0
FROM basedependencies AS leela
RUN git clone --depth=1 https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew
RUN mkdir ~/.linuxbrew/bin
RUN ln -s ~/.linuxbrew/Homebrew/bin/brew ~/.linuxbrew/bin
RUN eval $(~/.linuxbrew/bin/brew shellenv)
ENV PATH="~/.linuxbrew/bin/:$PATH"
ENV PATH="~/.linuxbrew/Homebrew/bin/:$PATH"
RUN ~/.linuxbrew/bin/brew install lc0 --verbose
########

FROM leela
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
