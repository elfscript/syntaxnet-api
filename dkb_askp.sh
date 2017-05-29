#!/bin/bash
ver=2.7
if [[ "$#" == "1" ]]; then
  ver=$1
fi
echo $ver
docker build -f Dockerfile_askp -t 3hdeng/syntax-api:askp . 
