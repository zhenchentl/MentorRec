#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-19 18:40:13
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import os
import sys
sys.path.append('..')
from RedisHelper.RedisHelper import RedisHelper
from util.param import *
from util.util import *

class newVec():
    """docstring for newVec"""
    def __init__(self):
        self.redis = RedisHelper()

    def reSaveNewVec(self):
        authors = self.redis.getAuthorList()
        index = 0
        for author in authors:
            if index % 1000 == 0:
                print index
            index += 1
            vecSet = self.redis.getAuthorVec(author)
            # print vecSet
            newVec = self.ProcWithTimeAndTopN(vecSet)
            for item, value in newVec.items():
                self.redis.addAuthorNewVec(author, item + ':' + str(value))

    def ProcWithTimeAndTopN(self, VecSet):
        d = dict()
        for item in VecSet:
            topic = item.split(':')[0]
            year = item.split(':')[1]
            value = item.split(':')[2]
            if int(year) >= PAPER_START_YEAR:
                d[topic + ':' + year] = float(value)
        d = sorted(d.iteritems(), key = lambda d:d[1], reverse = True)[:5]
        d = {item[0] : TimeFunctionLog10(int(item[0].split(':')[1])) * item[1] \
            for item in d}
        return d

if __name__ == '__main__':
    newVec = newVec()
    newVec.reSaveNewVec()
