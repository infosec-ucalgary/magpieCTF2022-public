FROM alpine

# ensure nodejs server can be run
RUN apk add --upgrade nodejs npm

RUN mkdir -p /var/www/html/js /var/www/html/css /var/www/html/data/emails && adduser -h /home/node/ node --disabled-password
COPY public/*.html /var/www/html/
ADD public/js /var/www/html/js
ADD public/css /var/www/html/css
ADD public/data/emails/ /var/www/html/data/emails/

WORKDIR /home/node

COPY userdata.json.default /var/www/html/data/userdata.json
COPY package.json index.js /home/node/
COPY public/data/*.json /var/www/html/data/

RUN npm install && chown -R node: /var/www/html

USER node

CMD ["npm", "start"]
