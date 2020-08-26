FROM node:12

RUN npm install -g artillery --allow-root --unsafe-perm=true
RUN npm install -g artillery-plugin-publish-metrics

COPY artillery-conf.yml /conf.yml

CMD artillery run /conf.yml

