FROM python:3.7-stretch

ENV API_URL https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file

WORKDIR /application

COPY requirement.txt .

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.9.1-amd64.deb

RUN dpkg -i filebeat-7.9.1-amd64.deb

COPY filebeat.yml /etc/filebeat

RUN mkdir /files

RUN mkdir /rebuild

RUN pip install -r requirement.txt --user

COPY target_minio.py .

COPY logging.conf .

CMD ["python", "target_minio.py"]