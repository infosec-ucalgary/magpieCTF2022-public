#!/bin/bash

OLD_PWD=$(pwd)
cd $(dirname $0)

sudo python3 rpi-client.py

cd $OLD_PWD
