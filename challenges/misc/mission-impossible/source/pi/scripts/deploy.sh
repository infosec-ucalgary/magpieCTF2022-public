#!/bin/bash

USER="dietpi"
HOST="zero.localdomain"
REMOTE_PATH="/home/dietpi/mission-impossible"

OLD_PWD=$(pwd)
cd $(dirname $0)

ssh ${USER}@${HOST} mkdir -p ${REMOTE_PATH}

# Upload rpi-client.
scp ../app/rpi-client.py ../app/run.sh ../app/rpi-client.service ${USER}@${HOST}:${REMOTE_PATH}

ssh ${USER}@${HOST} sudo cp ${REMOTE_PATH}/rpi-client.service /etc/systemd/system/rpi-client.service
ssh ${USER}@${HOST} sudo systemctl daemon-reload
ssh ${USER}@${HOST} sudo systemctl restart rpi-client.service

cd $OLD_PWD
