#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-27 14:23:01
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import os
import sys
sys.path.append('..')

from util.util import *
from util.param import *
import pickle
import random

class Citation():
    def __init__(self):
        self.redis = RedisHelper()

    def recom(self):
        targets = getTargetAuthor()
        recom_result = dict()
        recomlist = self.getRecomList()
        for index, target in enumerate(targets):
            print index
            count = 0
            recom = list()
            while True:
                item = random.choice(recomlist)
                if item not in recom:
                    recom.append(item)
                    count += 1
                    if count == 200:
                        break
            recom_result[target] = recom
        resultsave = open(PATH_CITATION_RECOM_LIST, 'wb')
        pickle.dump(recom_result, resultsave)
        resultsave.close()

    def getRecomList(self):
        authors = self.redis.getAuthorList()
        sim = dict()
        for author in authors:
            referedNum = 0
            papers = self.redis.getAuthorPapers(author)
            for paper in papers:
                if int(self.redis.getPaperYear(paper)) < TEST_DATA_YEAR:
                    referedNum += len(self.redis.getPaperRefered(paper))
            sim[author] = referedNum
        return sorted(sim.iteritems(), key = lambda d:d[1], reverse = True)[:1000]

if __name__ == '__main__':
    citation = Citation()
    citation.recom()
