FROM python:3.6

ENV TZ="America/Denver"
EXPOSE 5000

WORKDIR /root/

# pip installs
RUN pip3 install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


COPY aws-api.py .
COPY awsresources.py .

CMD python3 aws-api.py
