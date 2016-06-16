#! /usr/bin/python
# -*- coding: UTF-8 -*-

'''
  作者 : 王峰
  日期 : 2016-06-02
  描述 : 
'''

import os
import sys
import time
import urllib2
from urllib import quote

def cut(text):
    api_key="e4Z5n2c6PucP8WBOlgCAeNxkYhtOIvZo1jMHHQvH"
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    fmt= 'json'
    pattern = 'pos'
    url = "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,quote(text),fmt,pattern)
    urldata = {
            'api_key' : api_key,
            'text' : text,
            'format' : fmt,
            'pattern' : pattern
            }
    content = ''
    print url
    for i in range(3):
        try:
            result = urllib2.urlopen(url)
            content = result.read().strip()
            return content
        except:
            time.sleep(0.1*i)
            continue
    return content
if __name__ == '__main__':
    print cut('我是傻逼')
