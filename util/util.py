#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-13 18:06:13
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import sys
sys.path.append('..')
import math
from param import *
from RedisHelper.RedisHelper import *
import random
import math

def TimeFunctionLog10(year):
    return math.log(year - PAPER_START_YEAR + 2, 10)

def TimeFunctionLoge(year):
    return math.log(year - PAPER_START_YEAR + 2)

def TimeFunctionLine(year):
    return (year - PAPER_START_YEAR + 1)

def saveTargetAuthor():
    redis = RedisHelper()
    authors = redis.getAuthorList()
    count = 0
    author_ref_before = dict()
    author_ref_after = dict()
    target = list()
    for index, author in enumerate(authors):
        if index % 10000 == 0:
            print index
        papers = redis.getAuthorPapers(author)
        num = len(papers)
        if num >= TARGET_PAPER_NUM_MIN and num <= TARGET_PAPER_NUM_MAX:
            references_after, references_before = 0,0
            for paper in papers:
                if int(redis.getPaperYear(paper)) > TEST_DATA_YEAR:
                    references_after += len(redis.getPaperReferences(paper))
                else:
                    references_before += len(redis.getPaperReferences(paper))
            author_ref_after[author] = author_ref_after.setdefault(author, 0) + references_after
            author_ref_before[author] = author_ref_before.setdefault(author, 0) + references_before
    after_sorted = sorted(author_ref_after.iteritems(), key = lambda d:d[1], reverse = True)[:1000]
    print after_sorted[:200]
    for author, ref in after_sorted:
        if author_ref_before[author] > 1:
            print author, ref
            target.append(author)
            count += 1
            if count == 100:
                break
    print count

    # while True:
    #     author = random.choice(authors)
    #     papers = redis.getAuthorPapers(author)
    #     num = len(papers)
    #     if num >= TARGET_PAPER_NUM_MIN and num <= TARGET_PAPER_NUM_MAX:
    #         references_after, references_before = list(), list()
    #         for paper in papers:
    #             if int(redis.getPaperYear(paper)) > TEST_DATA_YEAR:
    #                 ref = list(redis.getPaperReferences(paper))
    #                 references_after.extend(ref)
    #             else:
    #                 ref = list(redis.getPaperReferences(paper))
    #                 references_before.extend(ref)
    #         if len(references_before) > 8 and len(references_after) > 4:
    #             if author not in target:
    #                 count += 1
    #                 print '********************',count
    #                 target.append(author)
    #                 if count == 10:
    #                     break
    with open(PATH_TARGET_AUTHOR, 'w') as fileWrite:
        s = ','.join(target)
        fileWrite.write(s)
        fileWrite.close()

def getTargetAuthor():
    redis = RedisHelper()
    with open(PATH_TARGET_AUTHOR, 'r') as fileReader:
        target = fileReader.read().split(',')
    fileReader.close()
    return target

def sim_distance_cos(p1, p2):
    '''p1和p2是dict的话，遍历会更迅速'''
    c = list(set(p1.keys()) & set(p2.keys()))
    ss = sum([float(p1[i]) * float(p2[i]) for i in c])
    sq1 = math.sqrt(sum([pow(float(p1[i]), 2) for i in p1]))
    sq2 = math.sqrt(sum([pow(float(p2[i]), 2) for i in p2]))
    if sq1 * sq2 != 0:
        return float(ss)/(sq1 * sq2)
    return 0.0
if __name__ == '__main__':
    saveTargetAuthor()
    # redis = RedisHelper()
    # papers = redis.getPaperList()
    # d = dict()
    # for paper in papers:
    #     year = redis.getPaperYear(paper)
    #     d[year] = d.setdefault(year, 0) + 1
    # print sorted(d.iteritems(), key = lambda d : d[0], reverse = True)

