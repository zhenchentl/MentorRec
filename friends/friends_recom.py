#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-27 08:42:35
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import sys
sys.path.append('..')
from util.util import *
from util.param import *
import pickle

class Friends():
    def __init__(self):
        self.redis = RedisHelper()

    def recom(self):
        targets = getTargetAuthor()
        recom_result = dict()
        for index, target in enumerate(targets):
            print index
            recom_result[target] = self.recom4Author(target)
        resultsave = open(PATH_FRIENDS_RECOM_LIST, 'wb')
        pickle.dump(recom_result, resultsave)
        resultsave.close()

    def recom4Author(self, target):
        coauthors = self.redis.getAuthorCoauthors(target)
        sim = dict()
        candidates = list()
        for coauthor in coauthors:
            papers = self.redis.getAuthorPapers(coauthor)
            refers = list()
            for paper in papers:
                if paper not in list(self.redis.getAuthorPapers(target)):
                    if int(self.redis.getPaperYear(paper)) < TEST_DATA_YEAR:
                        refers.extend(self.redis.getPaperReferences(paper))
            for refer in refers:
                candidates.extend(list(self.redis.getPaperAuthors(refer)))
        sim = dict.fromkeys(candidates, 0)
        for can in candidates:
            papers = self.redis.getAuthorPapers(can)
            referedNum = sum([len(self.redis.getPaperRefered(paper))
                             if int(self.redis.getPaperYear(paper)) < TEST_DATA_YEAR else 0
                             for paper in papers])
            sim[can] = referedNum
        return sorted(sim.iteritems(), key = lambda d:d[1], reverse = True)[:RECOM_TOP_N]

if __name__ == '__main__':
    friends = Friends()
    friends.recom()
