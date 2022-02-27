# What Is Meta?
### Category: Forensics
### Author: Sunny Mangat

## Description
The image looks clean... Is it really tho? 

## Hints
1. https://linux.die.net/man/1/exiftool
2. The comment section looks sus

## Solution
Use EXIFtool to view the metadata of the image using the command `exiftool "Forensics.png"`. There is encrypted text (Base 64) under the `comment` label. Toss that text into cyberchef and you'll get the flag.

## Flag
magpie{l00k_cl0ser_n3xt_t1m3}
