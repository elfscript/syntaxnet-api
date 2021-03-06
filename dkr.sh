#!/bin/bash
ver=dragnn
if [[ "$#" == "1" ]]; then
	  ver=$1
  fi
echo $ver

docker run -it --rm  --name myapi \
  -v $(pwd):/mnt/work  -w /mnt/work \
  -v $HOME/workspaces/ud_models:/mnt/ud_models \
  -p 8888:8888 \
  3hdeng/syntax-api:$ver \
  /bin/bash


#    -v $gitRepo:/opt/$USER/repos \
#    -e "OPTION_NAME=OPTION_VALUE" \
#  -v $HOME/workspaces/syntaxnet_wrapper:/mnt/syntaxnet_wrapper \

