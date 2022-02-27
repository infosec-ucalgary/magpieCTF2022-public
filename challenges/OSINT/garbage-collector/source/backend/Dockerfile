FROM node:latest
WORKDIR /app
COPY ./src/index.js /app
COPY ./src/package.json /app
ADD ./src/images /app/images
RUN npm install --only=production
CMD node index.js
