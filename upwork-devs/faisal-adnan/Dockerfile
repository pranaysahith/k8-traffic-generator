FROM node:12

RUN npm install -g artillery --allow-root --unsafe-perm=true

COPY load.yml /load.yml

CMD artillery run /load.yml

