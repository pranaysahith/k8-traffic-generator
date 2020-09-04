FROM egaillardon/jmeter-plugins:5.2.1-2.0.0

WORKDIR /mnt/workspace

# install Minio client
RUN curl --location --silent --show-error --output /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x /usr/bin/mc

# copy jmeter.sh
COPY jmeter.sh /mnt/workspace/.
RUN chmod +x /mnt/workspace/jmeter.sh
