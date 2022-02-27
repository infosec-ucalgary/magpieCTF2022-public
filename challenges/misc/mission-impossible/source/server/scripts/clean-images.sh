#!/bin/bash

docker rmi $(docker images -f "dangling=true" -q) 2>/dev/null

if [ $? -eq 1 ]; then
    echo "No images to clean."
fi
