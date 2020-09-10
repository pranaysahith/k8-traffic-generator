FROM python:3-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    mkdir /output
COPY . .
ENV API_URL https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file
CMD [ "python", "processor" ]