FROM python:3-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV ENDPOINT=play.min.io \
    ACCESS_KEY=Q3AM3UQ867SPQQA43P2F \
    SECRET_KEY=zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG \
    BUCKET_NAME=2063b651-92a3-4a20-a4a5-03a96e7c5a89 \
    PROCESSOR_IMAGE=yardenshoham/glasswall-rebuild-eval:process-mode-0 \
    DOWNLOADER_IMAGE=yardenshoham/local-rebuild-downloader
CMD [ "python", "dispatcher" ]