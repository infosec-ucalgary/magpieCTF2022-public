#!/bin/bash

OLD_PWD=$(pwd)
cd $(dirname $0)/../src

javac *.java

jar cvfm ../out/turn-key.jar manifest.txt *

cd $OLD_PWD
