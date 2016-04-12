#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-18 13:39:35
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import sys
sys.path.append('..')
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)
from RedisHelper.RedisHelper import RedisHelper
from param import *
import re
import pickle

rewords = "Computing|Data|Knowledge Discovery|Knowledge-Discovery|"\
    +"Artificial Intelligence|Social|Network|Information"

class ReadData():
    """Store the data into redis"""
    def __init__(self):
        self.redis = RedisHelper()
        self.paperID = 0
        self.venue = ''
        self.year = 1970
        self.references = list()
        self.d = dict()
        self.count = 0
        logging.info('starting.....')

    def clearVar(self):
        self.references = []
        self.venue = ''
        self.year = 1970

    def read(self):
        with open('../../datasets/DBLPOnlyCitationOct19.txt') as fileReader:
            logging.info('reading.....')
            for line in fileReader:
                if line[0] != '#':
                    self.count += 1
                    if self.count % 10000 == 0:
                        logging.info(self.count)
                    self.save2Redis()
                    self.clearVar()
                elif line[1] == 'c': # venue
                    self.venue = line.strip('\n\r')[2:]
                elif line[1] == 't': # year
                    self.year = line.strip()[2:]
                elif line[1] == 'i': # paperID
                    self.paperID = line.strip()[6:]
                elif line[1] == '%': # references
                    self.references.append(line.strip()[2:])

    def save2Redis(self):
        if re.search(rewords, self.venue):
            if self.paperID != '':
                if int(self.year) >= PAPER_START_YEAR:
                    if len(self.references) > 0 and  self.references[0] != '':
                        self.d[len(self.references)] = self.d.setdefault(len(self.references), 0) + 1
                    else:
                        self.d[0] = self.d.setdefault(0, 0) + 1

if __name__ == '__main__':
    # readData = ReadData()
    # readData.read()
    # print sorted(readData.d.iteritems(), key=lambda d : readData.d[1], reverse = True)
    fileRecomList = open(PATH_FRIENDS_RECOM_LIST, 'r')
    recomlist = pickle.load(fileRecomList)
    print recomlist
