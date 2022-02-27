#!/bin/bash

IMAGE_NAME=registry.digitalocean.com/infosec-registry/turn-key

OLD_PWD=$(pwd)
cd $(dirname $0)

./compile.sh

cd ..
docker build -t ${IMAGE_NAME} .
docker push ${IMAGE_NAME}

docker run -p 5555:5555 ${IMAGE_NAME}

cd $OLD_PWD
