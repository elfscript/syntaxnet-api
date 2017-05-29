#!/bin/bash
ver=dragnn
if [[ "$#" == "1" ]]; then
  ver=$1
fi
echo $ver
docker build -f Dockerfile_$ver  -t 3hdeng/syntax-api:$ver . 
