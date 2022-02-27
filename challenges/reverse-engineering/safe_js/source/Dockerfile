FROM alpine

RUN apk add --update nodejs npm

RUN mkdir -p /var/www/html/js /var/www/html/css &&\
      mkdir /home/node &&\
      adduser -h /home/node/ node --disabled-password &&\
      chown -R node:node /var/www/html

COPY index.html /var/www/html
ADD js /var/www/html/js
ADD css /var/www/html/css

COPY package.json index.js /home/node/
WORKDIR /home/node
USER node

CMD ["npm", "start"]
