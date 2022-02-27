#!/bin/bash

echo "Provisioning turn-key solve instance"

apt-get update
apt-get -y install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pwntools

echo "* * * * * /usr/bin/python3 /root/solve.py $1 $2 $3" > /root/root_crontab
crontab /root/root_crontab
