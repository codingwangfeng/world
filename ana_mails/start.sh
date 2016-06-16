#! /bin/bash

#########################################################
# 功能: 一个简单的脚本
# 日期 : 2016-06-02
#########################################################
export PS4='+[$(date "+%Y-%m-%d %H:%M:%S") +${SECONDS}s ${BASH_SOURCE} ${LINENO}] ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
set -x
if [ $# -ne 1 ];then
    echo "bash $0 mbox"
    exit 1
fi
python wc.py $1 | sort -t'	' -k2 -nr > word_count.txt 

