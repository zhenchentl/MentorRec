#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-04-13 18:28:26
# @Author  : Damon Chen (zhenchentl@gmail.com)
# @Link    : www.zhenchen.me
# @Version : $Id$

import redis

DB_PAPERID_YEAR = 0
DB_PAPERID_VENUE = 1
DB_PAPERID_TITLE = 2
DB_PAPERID_AUTHORS = 3
DB_PAPERID_ABSTRACT = 4
DB_PAPERID_REFERENCES = 5
DB_AUTHOR_PAPERIDS = 6
DB_AUTHOR_COAUTHORS = 7
DB_AUTHOR_VEC = 8
DB_PAPER_REFERED = 9
DB_DOC_AUTHOR_YEAR = 10
DB_AUTHOR_VEC_NEW = 11

IP = '172.11.250.186'
PORT = 6379

class RedisHelper():
    """docstring for RedisHelper"""
    def __init__(self):
        '''key-->value: The publicating year of paper'''
        self.paperYearDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPERID_YEAR)
        '''key-->value: The publicating venue of paper'''
        self.paperVenueDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPERID_VENUE)
        '''key-->value: The title of paper'''
        self.paperTitleDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPERID_TITLE)
        '''key-->set: The authors of paper'''
        self.paperAuthorsDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPERID_AUTHORS)
        '''key-->value: The abstract of paper'''
        self.paperAbstractDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPERID_ABSTRACT)
        '''key-->set: The recerences of paper'''
        self.paperReferencesDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPERID_REFERENCES)
        '''key-->set: The papers of one researcher'''
        self.authorPapersDB = redis.StrictRedis(IP, port = PORT, db = DB_AUTHOR_PAPERIDS)
        '''key-->set: The coauthor of one researcher'''
        self.authorCoauthorDB = redis.StrictRedis(IP, port = PORT, db = DB_AUTHOR_COAUTHORS)
        '''key-->set: The vector of One researcher'''
        self.authorVecDB = redis.StrictRedis(IP, port = PORT, db = DB_AUTHOR_VEC)
        '''key-->set: The refered list of one paper'''
        self.paperReferedDB = redis.StrictRedis(IP, port = PORT, db = DB_PAPER_REFERED)
        # '''key-->value: The docs of every author in each year'''
        # self.docsDB = redis.StrictRedis(IP, port = PORT, db = DB_DOCS)
        '''key-->value: The doc info, author and year'''
        self.docAuthorYear = redis.StrictRedis(IP, port = PORT, db = DB_DOC_AUTHOR_YEAR)
        '''key-->set: The modified vector of one researcher'''
        self.authorVecNewDB = redis.StrictRedis(IP, port = PORT, db = DB_AUTHOR_VEC_NEW)

    def addPaperYear(self, paperID, year):
        return self.paperYearDB.set(paperID, year)

    def addPaperVenue(self, paperID, venue):
        return self.paperVenueDB.set(paperID, venue)

    def addPaperTitle(self, paperID, title):
        return self.paperTitleDB.set(paperID, title)

    def addPaperAuthors(self, paperID, authors):
        return self.paperAuthorsDB.sadd(paperID, authors)

    def addPaperAbstract(self, paperID, abstract):
        return self.paperAbstractDB.set(paperID, abstract)

    def addPaperReferences(self, paperID, references):
        return self.paperReferencesDB.sadd(paperID, references)

    def addPaperRefered(self, paperID, referedID):
        return self.paperReferedDB.sadd(paperID, referedID)

    def addAuthorPapers(self, author, papers):
        return self.authorPapersDB.sadd(author, papers)

    def addAuthorCoauthor(self, author, coauthor):
        return self.authorCoauthorDB.sadd(author, coauthor)

    def addAuthorVec(self, author, VecItem):
        ''''VecItem-->topic1:year:value'''
        return self.authorVecDB.sadd(author, VecItem)

    def addAuthorNewVec(self, author, VecItem):
        '''VecItem-->topic1:year:value'''
        return self.authorVecNewDB.sadd(author, VecItem)

    def addDoc(self, index, doc):
        return self.docsDB.set(index, doc)

    def addDocAuthorYear(self, index, author, year):
        return self.docAuthorYear.set(index, author + ':' + str(year))

    def getAuthorList(self):
        return self.authorPapersDB.keys()

    def getPaperList(self):
        return self.paperVenueDB.keys()

    def getPaperYear(self, paperID):
        return self.paperYearDB.get(paperID)

    def getPaperVenue(self, paperID):
        return self.paperVenueDB.get(paperID)

    def getPaperTitle(self, paperID):
        return self.paperTitleDB.get(paperID)

    def getPaperAuthors(self, paperID):
        return self.paperAuthorsDB.smembers(paperID)

    def getPaperAbstract(self, paperID):
        return self.paperAbstractDB.get(paperID)

    def getPaperReferences(self, paperID):
        return self.paperReferencesDB.smembers(paperID)

    def getPaperRefered(self, paperID):
        return self. paperReferedDB.smembers(paperID)

    def getAuthorPapers(self, author):
        return self.authorPapersDB.smembers(author)

    def getAuthorCoauthors(self, author):
        return self.authorCoauthorDB.smembers(author)

    def getAuthorVec(self, author):
        return self.authorVecDB.smembers(author)

    def getAuthorNewVec(self, author):
        return self.authorVecNewDB.smembers(author)

    def getDoc(self, index):
        return self.docsDB.get(index)

    def getAllDocIndex(self):
        return self.docsDB.keys()

    def getDocAuthorYear(self, index):
        return self.docAuthorYear.get(index)
