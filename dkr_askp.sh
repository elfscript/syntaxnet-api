#!/bin/bash

docker run -it --rm  --name myapi \
  -v $(pwd):/mnt/work  -w /mnt/work \
  -v $HOME/workspaces/ud_models:/mnt/ud_models \
  -p 8888:8888 \
  gliacloud/syntaxnet \
  /bin/bash


#    -v $gitRepo:/opt/$USER/repos \
#    -e "OPTION_NAME=OPTION_VALUE" \
