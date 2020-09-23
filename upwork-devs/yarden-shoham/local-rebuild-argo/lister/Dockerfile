FROM python:3-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV ENDPOINT=play.min.io \
    ACCESS_KEY=Q3AM3UQ867SPQQA43P2F \
    SECRET_KEY=zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG \
    BUCKET_NAME=20200916104820-mydumper
CMD [ "python", "lister" ]