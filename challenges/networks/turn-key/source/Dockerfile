FROM openjdk:8-alpine

EXPOSE 5555

ENV SERVER_NUMBER=0
ENV NUMBER_OF_SERVERS=3
ENV KEY_PERIOD=700
ENV PROTOCOL_TIME=300

WORKDIR /app
COPY docker-entrypoint.sh /usr/local/bin

COPY ./out/turn-key.jar /app/turn-key.jar

ENTRYPOINT ["docker-entrypoint.sh"]
