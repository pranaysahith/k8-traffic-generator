FROM mhart/alpine-node:12

RUN npm install -g artillery --allow-root --unsafe-perm=true
RUN npm install -g artillery-plugin-publish-metrics
RUN npm install -g artillery-plugin-expect

WORKDIR /mnt/workspace

RUN wget -qO /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x /usr/bin/mc

COPY artillery.sh /mnt/workspace/.
RUN chmod +x /mnt/workspace/artillery.sh

