#!/bin/sh
mc --insecure alias set minio https://${MINIO_SERVICE_HOST}:${MINIO_SERVICE_PORT_HTTP_MINIO} "${MINIO_ACCESS_KEY}" "${MINIO_SECRET_KEY}"
mkdir -p jmeter-workdir-${HOSTNAME}
sh apache-jmeter-5.3/bin/jmeter -n -Jjmeterengine.force.system.exit=true \
                                -t /etc/conf/jmeter-conf.gmx \
                                -l jmeter-workdir-${HOSTNAME}/jmeter_result-${HOSTNAME}.jtl \
                                -j jmeter-workdir-${HOSTNAME}/jmeter_log-${HOSTNAME}.jtl \
                                -e -o jmeter-workdir-${HOSTNAME}/dashboard

mc --insecure cp --recursive jmeter-workdir-${HOSTNAME} minio/jmeter/
