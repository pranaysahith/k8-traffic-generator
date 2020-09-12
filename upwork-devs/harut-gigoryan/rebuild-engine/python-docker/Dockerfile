#FROM docker.elastic.co/beats/filebeat:7.9.1
FROM python:3.7-stretch

WORKDIR /application

COPY requirement.txt .

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.9.1-amd64.deb

RUN dpkg -i filebeat-7.9.1-amd64.deb

COPY filebeat.yml /etc/filebeat

RUN mkdir /files

RUN pip install -r requirement.txt --user

COPY target_minio.py .

COPY logging.conf .

CMD ["python", "target_minio.py"]