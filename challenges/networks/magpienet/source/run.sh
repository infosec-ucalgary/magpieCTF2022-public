#!/bin/bash
# 

set -e

python3 /app/node.py 46442 0 &
python3 /app/node.py 46487 1 &
python3 /app/node.py 46441 2 &
python3 /app/node.py 46301 3 &
python3 /app/node.py 46316 4 &
python3 /app/node.py 46102 5 &
python3 /app/node.py 46911 6 &
python3 /app/node.py 46382 7 &
python3 /app/file.py 46382 41111 & # Node 7
python3 /app/encrypt.py 46102 41122 & # Node 6
python3 /app/flag.py 46911 49988 # Node 5, docker loops on this
