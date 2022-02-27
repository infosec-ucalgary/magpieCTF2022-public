FROM alpine

# ensure nodejs server can be run
RUN apk add --upgrade nodejs npm

RUN mkdir -p /var/www/html/js /var/www/html/css /var/www/html/data/ && adduser -h /home/node/ node --disabled-password
COPY public/*.html /var/www/html/
ADD public/js /var/www/html/js
ADD public/css /var/www/html/css
ADD public/data /var/www/html/data

WORKDIR /home/node

COPY package.json index.js /home/node/

RUN npm install && chown -R node: /var/www/html

USER node

CMD ["npm", "start"]
