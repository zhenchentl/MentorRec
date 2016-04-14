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
        self.authorReferedNum = dict()
        authors = self.redis.getAuthorList()
        for author in authors:
            referedNum = 1.0
            papers = self.redis.getAuthorPapers(author)
            referedNum = sum([len(self.redis.getPaperRefered(paper)) for paper in papers])
            self.authorReferedNum[author] = referedNum

    def recom(self):
        authors = self.redis.getAuthorList()
        authorVec = dict()
        for author in authors:
            authorVec[author] = self.redis.getAuthorVec(author)
        targets = getTargetAuthor()
        recom_result = dict() # target-->recom author : simlarity
        for index, target in enumerate(targets):
            print index
            recom_result[target] = self.recom4Author(target,authors,authorVec)
            print recom_result[target]
        resultsave = open(PATH_CONTENT_RECOM_LIST, 'wb')
        pickle.dump(recom_result, resultsave)
        resultsave.close()

    def recom4Author(self, target,authors,authorVec):
        sim = dict()
        for author in authors:
            sim[author] = self.similarity(authorVec[target],authorVec[author])
        return sorted(sim.iteritems(), key = lambda d : d[1],\
                      reverse = True)[:RECOM_TOP_N]

    def similarity(self, author1Vec, author2Vec):
        a1 = dict()
        a2 = dict()
        for vecItem in author1Vec:
            topic, year, value = vecItem.split(':')
            d = a1.setdefault(topic, 0)
            a1[topic] = d + float(value)
        for vecItem in author2Vec:
            topic, year, value = vecItem.split(':')
            d = a2.setdefault(topic, 0)
            a2[topic] = d + float(value)
        return sim_distance_cos(a1, a2)
if __name__ == '__main__':
    recom = Recom()
    recom.recom()
