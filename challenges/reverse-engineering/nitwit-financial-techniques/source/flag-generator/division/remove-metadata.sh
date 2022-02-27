#!/bin/bash

for filename in /mnt/c/Users/Jer/Documents/magpieCTF-2022/challenges/reverse-engineering/hard-rev/division/*.png; do
	echo "${filename##*/}"
	exiftool -all= "${filename##*/}"
done
