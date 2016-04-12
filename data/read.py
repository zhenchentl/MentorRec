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
import re

rewords = "Computing|Data|Knowledge Discovery|Knowledge-Discovery|"\
    +"Artificial Intelligence|Social|Network|Information"

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
                    self.title = line.strip('\n\r')[2:]
                elif line[1] == '@': # authors
                    self.authors.extend(line.strip('\n\r')[2:].split(','))
                elif line[1] == 't': # year
                    self.year = line.strip()[2:]
                elif line[1] == 'c': # venue
                    self.venue = line.strip('\n\r')[2:]
                elif line[1] == 'i': # paperID
                    self.paperID = line.strip()[6:]
                elif line[1] == '%': # references
                    self.references.append(line.strip()[2:])
                elif line[1] == '!': # abstract
                    self.abstract = line.strip('\n\r')[2:]

    def save2Redis(self):
        if re.search(rewords, self.venue):
            if self.paperID != '' and self.year != '':
                if int(self.year) >= PAPER_START_YEAR:
                    self.redis.addPaperYear(self.paperID, self.year)
                    self.redis.addPaperVenue(self.paperID, self.venue)
                    self.redis.addPaperTitle(self.paperID, self.title)
                    self.redis.addPaperAbstract(self.paperID, self.abstract)
                    if self.references[0] != '':
                        for reference in self.references:
                            self.redis.addPaperReferences(self.paperID, reference)
                            self.redis.addPaperRefered(reference, self.paperID)
                    for author in self.authors:
                        self.redis.addAuthorPapers(author, self.paperID)
                        self.redis.addPaperAuthors(self.paperID, author)
                    if len(self.authors) > 1:
                        for i in range(len(self.authors)):
                            self.redis.addAuthorPapers(self.authors[i], self.paperID)
                            for j in range(i + 1, len(self.authors)):
                                self.redis.addAuthorCoauthor(self.authors[i], self.authors[j])
                                self.redis.addAuthorCoauthor(self.authors[j], self.authors[i])
class Docs():
    """docstring for Docs"""
    def __init__(self):
        logging.info('conduct docs firstly')
        self.redis = RedisHelper()

    def conductDocs(self):
        fileWtriter = file(PATH_DOC_AUTHOR, 'w')
        authorList = self.redis.getAuthorList()
        authorDoc = dict() # year-->docs. the docs of an author in every year
        index = 0
        for author in authorList:
            authorDoc = {}
            papers = self.redis.getAuthorPapers(author)
            for paper in papers:
                year = self.redis.getPaperYear(paper)
                if int(year) <= TEST_DATA_YEAR: # we only use the data in ten years
                    content = self.redis.getPaperAbstract(paper)
                    if len(content) < 3: # if there is no abstract,return title
                        content = self.redis.getPaperTitle(paper)
                    doc = authorDoc.setdefault(year, "")
                    authorDoc[year] = doc + content
            for year, doc in authorDoc.items():
                if index % 10000 == 0: print index
                fileWtriter.write(doc + '\n')
                self.redis.addDocAuthorYear(index, author, year)
                index += 1
        fileWtriter.close()

if __name__ == '__main__':
    read = ReadData()
    read.read()
    docs = Docs()
    docs.conductDocs()
