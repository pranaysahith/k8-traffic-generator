FROM adoptopenjdk:8-jre-openj9-bionic

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y wget 

RUN wget -qO apache-jmeter-5.3.tgz https://artfiles.org/apache.org//jmeter/binaries/apache-jmeter-5.3.tgz 

WORKDIR /mnt/workspace
COPY gws.jmx .
COPY apache-jmeter-5.3.tgz .

RUN tar xzf apache-jmeter-5.3.tgz
CMD sh apache-jmeter-5.3/bin/jmeter -n -Jjmeterengine.force.system.exit=true -t gws.jmx -l gws_result.xml -e -o out