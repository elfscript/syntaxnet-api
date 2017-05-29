#!/bin/bash

#cd `pip -V | sed -e "s/.*from //" -e "s/ (.*//"`
#cd /usr/local/lib/python2.7/dist-packages
#cd syntaxnet_wrapper/models/syntaxnet
cd /opt/tensorflow/syntaxnet
#/syntaxnet/models/parsey_universal
echo 'Bob brought the pizza to Alice.' | bash syntaxnet/parse.sh /mnt/ud_models/English 2> /dev/null
echo '球 從 天上 掉 下來' | bash syntaxnet/parse.sh  /mnt/ud_models/Chinese 2> /dev/null
echo '球從天上掉下來' | bash syntaxnet/tokenize_zh.sh  /mnt/ud_models/Chinese 2> /dev/null
