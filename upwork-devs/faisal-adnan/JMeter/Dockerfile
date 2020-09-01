FROM adoptopenjdk:8-jre-openj9-bionic

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y wget 

WORKDIR /mnt/workspace

RUN wget -qO apache-jmeter-5.3.tgz https://artfiles.org/apache.org//jmeter/binaries/apache-jmeter-5.3.tgz 

# install JMeter
RUN tar xzf apache-jmeter-5.3.tgz

# install Minio client
RUN wget -qO /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x /usr/bin/mc

# copy jmeter.sh
COPY jmeter.sh /mnt/workspace/.
RUN chmod +x /mnt/workspace/jmeter.sh
