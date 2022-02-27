#!/bin/bash

USER="root"
HOST="143.198.224.170"
REMOTE_PATH="/root/omni-flags"

IMAGE_NAME="omni-flags"

OLD_PWD=$(pwd)
cd $(dirname $0)

# Build the docker image.
NODE_ENV=production yarn gatsby build
systemctl is-active --quiet docker || systemctl start docker
docker build -t ${IMAGE_NAME} .

# Save and compress image to tarball.
docker save -o ${IMAGE_NAME}.tar ${IMAGE_NAME}
gzip -f ${IMAGE_NAME}.tar

# Upload deploy files.
ssh ${USER}@${HOST} mkdir -p ${REMOTE_PATH}
scp ${IMAGE_NAME}.tar.gz docker-compose.yml clean-images.sh ${USER}@${HOST}:${REMOTE_PATH}

# Deploy new docker image.
ssh ${USER}@${HOST} docker load -i ${REMOTE_PATH}/${IMAGE_NAME}.tar.gz
ssh ${USER}@${HOST} docker-compose -f ${REMOTE_PATH}/docker-compose.yml up -d

# Clean up unused docker images.
ssh ${USER}@${HOST} ${REMOTE_PATH}/clean-images.sh

cd $OLD_PWD
