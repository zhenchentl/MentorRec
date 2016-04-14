import sys
sys.path.append('..')
from util import *
from param import *
import pickle

def academicLevel():
    mRedis = RedisHelper()
    authorReferedNum = dict()
    fileRecomList = open(PATH_CONTENT_RECOM_LIST, 'r')
    recomlist = pickle.load(fileRecomList)
    for target in recomlist.keys():
        for author, sim in recomlist[target]:
            if not authorReferedNum.has_key(author):
                papers = mRedis.getAuthorPapers(author)
                authorReferedNum[author] = sum([len(mRedis.getPaperRefered(paper)) for paper in papers])
    for length in range(1,RECOM_TOP_N, 3):
        referedNum = 0
        for target in recomlist.keys():
            for author, sim in recomlist[target][0:length]:
                referedNum += authorReferedNum[author]
        print referedNum / (1.0 * len(recomlist.keys()) * length)

if __name__ == '__main__':
    academicLevel()
