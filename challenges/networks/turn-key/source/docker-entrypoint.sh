#!/bin/sh

exec java -jar turn-key.jar 5555 ${SERVER_NUMBER} ${NUMBER_OF_SERVERS} ${KEY_PERIOD} ${PROTOCOL_TIME}
