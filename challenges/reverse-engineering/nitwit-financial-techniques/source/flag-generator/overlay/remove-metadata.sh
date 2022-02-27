#!/bin/bash

for filename in /mnt/c/Users/Jer/Documents/magpieCTF-2022/challenges/reverse-engineering/hard-rev/overlay/*.png; do
        echo "${filename##*/}"
        exiftool -all= "${filename##*/}"
done
