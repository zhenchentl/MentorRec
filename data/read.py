#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-13 10:56:04
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import sys
sys.path.append('..')
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                    level=logging.INFO)
from RedisHelper.RedisHelper import RedisHelper
from util.param import *

class ReadData():
    """Store the data into redis"""
    def __init__(self):
        self.redis = RedisHelper()
        self.title = str()
        self.authors = list()
        self.year = 1970
        self.venue = str()
        self.paperID = 0
        self.references = list()
        self.abstract = str()
        self.authorCoauthor = dict()
        self.count = 0
        logging.info('starting.....')

    def clearVar(self):
        self.title = ""
        self.venue = ""
        self.abstract = ""
        self.authors = []
        self.references = []
        self.authorCoauthor = {}
        self.year = 1970

    def read(self):
        with open(PATH_DATASET_TXT) as fileReader:
            logging.info('reading.....')
            for line in fileReader:
                if line[0] != '#':
                    self.count += 1
                    if self.count % 10000 == 0:
                        logging.info(self.count)
                    self.save2Redis()
                    self.clearVar()
                elif line[1] == '*': # title
                    self.title = line.strip('\n')[2:]
                elif line[1] == '@': # authors
                    self.authors.extend(line.strip('\n')[2:].split(','))
                elif line[1] == 't': # year
                    self.year = line.strip('\n')[2:]
                elif line[1] == 'c': # venue
                    self.venue = line.strip('\n')[2:]
                elif line[1] == 'i': # paperID
                    self.paperID = line.strip('\n')[6:]
                elif line[1] == '%': # references
                    self.references.append(line.strip('\n')[2:])
                elif line[1] == '!': # abstract
                    self.abstract = line.strip('\n')[2:]

    def save2Redis(self):
        self.redis.addPaperYear(self.paperID, self.year)
        self.redis.addPaperVenue(self.paperID, self.venue)
        self.redis.addPaperTitle(self.paperID, self.title)
        self.redis.addPaperAbstract(self.paperID, self.abstract)
        self.redis.addPaperReferences(self.paperID, self.references)
        for author in self.authors:
            self.redis.addAuthorPapers(author, self.paperID)
        if len(self.authors) > 1:
            for i in range(len(self.authors)):
                self.redis.addAuthorPapers(self.authors[i], self.paperID)
                self.redis.addAuthorCoauthor(self.authors[i], \
                                             self.authors[:i] + self.authors[i + 1:])
if __name__ == '__main__':
    read = ReadData()
    read.read()
