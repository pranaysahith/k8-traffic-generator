FROM egaillardon/jmeter-plugins:5.2.1-2.0.0 as jmeter

FROM peltops/icap_service:0.0.1 AS icap
RUN /usr/local/c-icap/bin/c-icap-client -VV

RUN apt-get install -y software-properties-common
RUN apt-get update
RUN apt-get install -y curl wget

WORKDIR /mnt/workspace

# install Minio client
RUN curl --location --silent --show-error --output /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x /usr/bin/mc

# copy jmeter.sh
COPY jmeter.sh /mnt/workspace/.
RUN chmod +x /mnt/workspace/jmeter.sh

COPY --from=jmeter /opt/apache-jmeter-5.2.1 /opt/apache-jmeter-5.2.1

RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add -
RUN add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
RUN apt-get install -y adoptopenjdk-8-hotspot
RUN java -version
RUN echo $JAVA_HOME

ENV JAVA_HOME=/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64 \
    PATH="/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64/bin:$PATH" \
    PATH="/opt/apache-jmeter-5.2.1/bin:$PATH" 

RUN jmeter -v