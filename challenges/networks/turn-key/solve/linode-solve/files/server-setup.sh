#!/bin/bash

pip3 install requests
pip3 install pycryptodome
pip3 install prometheus_client

nohup /usr/bin/python3 /root/server.py &
