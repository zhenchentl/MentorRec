#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-20 17:03:55
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import os
import sys
sys.path.append('..')
from util.util import *
from util.param import *
import pickle

class Perform():
    """docstring for Perform"""
    def __init__(self):
        self.redis = RedisHelper()

    def getRecomList(self):
        fileRecomList = open(PATH_RECOM_LIST, 'r')
        recomlist = pickle.load(fileRecomList)
        return recomlist

    def getTargetCitated(self, author):
        papers = self.redis.getAuthorPapers(author)
        citatedAuthors = list()
        for paper in papers:
            year = int(self.redis.getPaperYear(paper))
            if year > TEST_DATA_YEAR:
                citatedAuthors.extend(self.redis.getPaperAuthors(paper))
        return citatedAuthors

    def getEvaluation(self, citatedAuthors, recomlist):
        recomLength = len(recomlist)
        citatedlength = len(citatedAuthors)
        hit = len(set(citatedAuthors) & set(recomlist))
        # print recomLength, citatedlength, hit
        precision = 1.0 * hit / recomLength if recomLength > 0 else 0.0
        recall = 1.0 * hit / citatedlength if citatedlength > 0 else 0.0
        F1 = 2 * precision * recall / (precision + recall) \
            if precision + recall > 0 else 0
        return precision, recall, F1

    def performance(self):
        recomlist = self.getRecomList()
        targetNum = len(recomlist)
        for length in range(1,RECOM_TOP_N, 3):
            precision, recall, F1 = 0, 0, 0
            for target in recomlist.keys():
                citatedAuthors = self.getTargetCitated(target)
                recom = [rec[0] for rec in recomlist[target][1: length + 1]]
                p, r, f = self.getEvaluation(citatedAuthors, recom)
                precision += p
                recall += r
                F1 += f
            print precision / targetNum, recall / targetNum, F1 / targetNum
            # break



if __name__ == '__main__':
    perform = Perform()
    perform.performance()
