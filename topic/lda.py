#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-15 14:52:30
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import sys
sys.path.append('..')
from util.param import *
import logging
from gensim import corpora, models
from RedisHelper.RedisHelper import RedisHelper
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)

class baselda():
    """docstring for baselda"""
    def __init__(self):
        logging.info("init starting...")
        self.redis = RedisHelper()
        self.docs = list()
        for line in open(PATH_DOC_AUTHOR, 'r'):
            self.docs.append(line.strip('\n').split())
        logging.info("init ending...")

    def lda_setp1(self):
        '''Step1'''
        dictionary = corpora.Dictionary(self.docs)
        logging.info("store the dictionary, for future reference.")
        dictionary.save_as_text(PATH_LDA_DIC)
        corpus = [dictionary.doc2bow(doc) for doc in self.docs]
        logging.info("store to disk, for later use.")
        corpora.MmCorpus.serialize(PATH_LDA_MM, corpus)

    def lda_step2(self):
        '''Step2'''
        logging.info("load Dictionary.")
        id2word = corpora.Dictionary.load_from_text(PATH_LDA_DIC)
        logging.info("load corpus iterator.")
        mm = corpora.MmCorpus(PATH_LDA_MM)
        logging.info('LDA Start.')
        lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, \
            num_topics=LDA_CLUSTER_NUM, update_every=1, chunksize=10000, passes=1)
        logging.info('LDA End')

        corpus_lda = list(lda[mm])
        self.saveVec(corpus_lda)

    def saveVec(self, corpus_lda):
        print len(corpus_lda)
        for DocId in range(len(corpus_lda)):
            # print DocId
            author, year = self.redis.getDocAuthorYear(DocId).split(':')
            for topic, value in corpus_lda[DocId]:
                self.redis.addAuthorVec(author, str(topic) + ':' + str(year) + \
                                        ':' + str(value))
        self.docs = []
        corpus_lda = []

if __name__ == '__main__':
    baselda = baselda()
    # step1:
    baselda.lda_setp1()
    # step2:
    baselda.lda_step2()
