#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-12 15:17:55
# @Author  : Damon Chen (Damon@zhenchen.me)
# @Link    : www.zhenchen.me
# @Version : $Id$
# @Description:

import os
import sys
sys.path.append('..')
from util.util import *
from util.param import *
from operator import itemgetter
import networkx as nx
from RedisHelper.RedisHelper import *
import pickle
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

class Graph(object):
    """docstring for Graph"""
    def __init__(self):
        self.graph = nx.Graph()

    def getGraph(self):
        mRedis = RedisHelper()
        count = 0
        for author in mRedis.getAuthorList():
            count += 1
            if count % 1000 == 0:
                print count
            for coau in mRedis.getAuthorCoauthors(author):
                if min(int(t) for t in mRedis.getAuCoauTime(author + ':' + coau)) < TEST_DATA_YEAR:
                    self.graph.add_edge(author, coau)
        logging.info('load graph done!')
        logging.info('nodes:' + str(self.graph.number_of_nodes()))
        logging.info('edges:' + str(self.graph.number_of_edges()))
        return self.graph

class Randomwalk():
    def __init__(self):
        self.S =dict()
    def PageRank(self, graph, current_node, damping_factor = 0.8,\
        max_iterations = 20, min_delta = 0.0001):
        nodes = graph.nodes()
        graph_size =graph.number_of_nodes()
        pagerank = dict.fromkeys(nodes, 0)
        pagerank[current_node] = 1.0
        min_value = damping_factor / graph_size
        for i in range(max_iterations):
            diff = 0
            for node in nodes:
                rank = min_value
                for referring_page in graph.neighbors(node):
                    rank += damping_factor * pagerank[referring_page] / \
                    graph.degree(referring_page)
                diff += abs(pagerank[node] - rank)
                pagerank[node] = rank
            pagerank[current_node] += 1 - damping_factor
            if diff < min_delta:
                break
        logging.info('itertimes:' + str(i))
        return pagerank

def recommender():
    graph = Graph().getGraph()
    targets = getTargetAuthor()
    mRedis = RedisHelper()
    recom_dict = dict()
    rw = Randomwalk()
    for index, author in enumerate(targets):
        logging.info(str(index))
        pagerank = rw.PageRank(graph, author)
        papers = mRedis.getAuthorPapers(author)
        connedCoaus = list()
        for paper in papers:
            if int(mRedis.getPaperYear(paper)) < TEST_DATA_YEAR:
                refers =mRedis.getPaperReferences(paper)
                for refer in refers:
                    connedCoaus.extend(mRedis.getPaperAuthors(refer))
        for node in pagerank.keys():
            if node in connedCoaus:
                pagerank[node] = 0.0
        recom_dict[author] = sorted(pagerank.iteritems(), key = lambda d:d[1], reverse = True)[:RECOM_TOP_N]
    resultsave = open(PATH_RWR_RECOM_LIST, 'wb')
    pickle.dump(recom_dict, resultsave)
    resultsave.close()

if __name__ == '__main__':
    recommender()


