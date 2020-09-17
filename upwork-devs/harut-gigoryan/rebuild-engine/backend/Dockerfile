FROM python:3-alpine
EXPOSE 5000
WORKDIR /usr/src/app
COPY requirements.txt .
RUN mkdir -p backend/static && pip install -r requirements.txt
COPY . .
ENV API_URL=https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file \
    PROCESSOR_IMAGE=ggrig/k8-traffic:re_processor
CMD [ "python", "backend" ]