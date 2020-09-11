FROM python:3.7-stretch

WORKDIR /application

COPY requirement.txt .

RUN mkdir /files

RUN useradd -u 6000 -m minio_tester 

RUN chown minio_tester. /application -R

RUN chown minio_tester. -R /files

USER minio_tester

RUN pip install -r requirement.txt --user

COPY target_minio.py .

COPY logging.conf .

CMD ["python", "target_minio.py"]