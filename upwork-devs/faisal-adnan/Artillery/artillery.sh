#!/bin/sh
mc --insecure alias set minio https://${MINIO_SERVICE_HOST}:${MINIO_SERVICE_PORT_HTTP_MINIO} "${MINIO_ACCESS_KEY}" "${MINIO_SECRET_KEY}"
artillery run -o report.json /etc/conf/artillery-conf.yml
artillery report -o report-${HOSTNAME}.html report.json
mc --insecure cp report-${HOSTNAME}.html minio/artillery
