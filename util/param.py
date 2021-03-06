#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-14 10:11:03
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import os


PAPER_START_YEAR = 2000
TEST_DATA_YEAR = 2009

LDA_CLUSTER_NUM = 200
VEC_TOP_N = 50
RECOM_TOP_N = 200


# TARGET_PAPER_NUM_MIN, TARGET_PAPER_NUM_MAX = 2,5
TARGET_PAPER_NUM_MIN, TARGET_PAPER_NUM_MAX = 6,25
# TARGET_PAPER_NUM_MIN, TARGET_PAPER_NUM_MAX = 26,100

PATH_DATASET_TXT = '../../datasets/publications.txt'
PATH_DOC_AUTHOR = '../../datasets/docs.txt'
PATH_LDA_DIC = '../../datasets/ldf.dic'
PATH_LDA_MM = '../../datasets/ldf.mm'
PATH_TARGET_AUTHOR = '../util/target_' + str(TARGET_PAPER_NUM_MIN) + '_' \
    + str(TARGET_PAPER_NUM_MAX) + '.txt'
PATH_RECOM_LIST = '../util/recomList' + str(TARGET_PAPER_NUM_MIN) + '_' \
    + str(TARGET_PAPER_NUM_MAX) + '_logE_200_50' + '.txt'
PATH_FRIENDS_RECOM_LIST = '../util/friendsRecomList' + str(TARGET_PAPER_NUM_MIN) + '_' \
    + str(TARGET_PAPER_NUM_MAX) + '.txt'
PATH_CITATION_RECOM_LIST = '../util/citationRecomList' + str(TARGET_PAPER_NUM_MIN) + '_' \
    + str(TARGET_PAPER_NUM_MAX) + '.txt'
PATH_RWR_RECOM_LIST = '../util/rwrRecomList' + str(TARGET_PAPER_NUM_MIN) + '_' \
    + str(TARGET_PAPER_NUM_MAX) + '.txt'
PATH_CONTENT_RECOM_LIST = '../util/contentRecomList' + str(TARGET_PAPER_NUM_MIN) + '_' \
    + str(TARGET_PAPER_NUM_MAX) + '.txt'
