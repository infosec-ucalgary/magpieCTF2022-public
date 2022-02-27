#!/bin/bash

OLD_PWD=$(pwd)
cd $(dirname $0)

bootprint openapi ./swagger.json dist
html-inline dist/index.html > api-docs.html

cd ${OLD_PWD}
