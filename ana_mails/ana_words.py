#! /usr/bin/python
# -*- coding: UTF-8 -*-

'''
  作者 : 王峰
  日期 : 2016-06-03
  描述 : 
'''

import os
import sys
import json

class Opt:
    def __init(self,argv):
        pass
    def __str__(self):
        pass

def usage():
    print 'Usage:'

def parse_argv():
    if len(sys.argv) < 1:
        print "param num error"
        sys.exit(-1)

def run():
    n_cnt = {}
    obj = json.loads(open('seg.txt').read())
    for i in obj:
        words = i[0][0]
        for w in words:
            tp = w["pos"]
            word = w["cont"]
            if tp != 'v': continue
            if word not in n_cnt: n_cnt[word] = 0
            n_cnt[word] += 1
    for i in n_cnt:
        print ('%s\t%s' % (i, n_cnt[i])).encode('utf-8')
if __name__ == '__main__':
    parse_argv()
    run()

