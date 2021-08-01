FROM amazonlinux:2 AS basedependencies

ENV TZ="America/Denver"
EXPOSE 5000

WORKDIR /root/

# pip installs
RUN yum install python3 python3-pip -y
RUN pip3 install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


FROM basedependencies AS flask
COPY aws-api.py .
COPY awsresources.py .

ENTRYPOINT ["python3", "aws-api.py"]