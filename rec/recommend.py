#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-20 11:05:21
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import sys
sys.path.append('..')
from util.util import *
from util.param import *
import pickle

class Recom():
    """docstring for Recom"""
    def __init__(self):
        self.redis = RedisHelper()

    def recom(self):
        authors = self.redis.getAuthorList()
        targets = getTargetAuthor()
        recom_result = dict() # target-->recom author : simlarity
        for index, target in enumerate(targets):
            print index
            recom_result[target] = self.recom4Author(target)
        resultsave = open(PATH_RECOM_LIST, 'wb')
        pickle.dump(recom_result, resultsave)
        resultsave.close()

    def recom4Author(self, target):
        authors = self.redis.getAuthorList()
        sim = dict()
        for author in authors:
            papers = self.redis.getAuthorPapers(author)
            referedNum = sum([len(self.redis.getPaperRefered(paper)) for paper in papers])
            sim[author] = referedNum * self.similarity(self.redis.getAuthorNewVec(target),\
                                          self.redis.getAuthorNewVec(author))
        return sorted(sim.iteritems(), key = lambda d : d[1],\
                      reverse = True)[:RECOM_TOP_N]

    def similarity(self, author1Vec, author2Vec):
        a1 = dict()
        a2 = dict()
        for vecItem in author1Vec:
            topic, year, value = vecItem.split(':')
            d = a1.setdefault(year, {})
            d[topic] = value
        for vecItem in author2Vec:
            topic, year, value = vecItem.split(':')
            d = a2.setdefault(year, {})
            d[topic] = value
        return sum(sim_distance_cos(a1[year], a2[year]) \
                   for year in set(a1.keys()) & set(a2.keys()))
if __name__ == '__main__':
    recom = Recom()
    recom.recom()
