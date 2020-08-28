FROM node:10

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
#COPY package*.json ./

#RUN useradd -m user
#USER user
#RUN echo $HOME

RUN mkdir /root/.log.io
COPY server.json /root/.log.io/

COPY net-logger.jc .

#RUN npm install
RUN npm install -g log.io

# Bundle app source
#COPY . .

#EXPOSE 16688
CMD [ "log.io-server" ]
#CMD [ "node", "net-logger.jc" ]
