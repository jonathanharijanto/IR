import json
import pprint
from collections import defaultdict, OrderedDict
import math
import re
import operator
from difflib import SequenceMatcher
import numpy as np

from Indexer import query_index_better

# old for milestone 2
def query_index(input, index_dict, url_dict):
    query = re.sub(r'\W', ' ', input).lower().split()
    resultList = []
    for q in query:
        if q in index_dict:
            resultList.append(index_dict[q])

    #print resultList
    #print len(resultList)
    intersectKeys = set(resultList[0].keys())
    #print intersectKeys

    for r in resultList[1:]:
        intersectKeys &= set(r.keys())

    #print intersectKeys

    intersectDict = OrderedDict()
    for key in intersectKeys:
        intersectDict[key] = []
        for r in resultList:
            if key in r:
                intersectDict[key].extend(sorted(r[key]))
    #print intersectDict

    i = 0
    resultURLs = []
    for key, positions in intersectDict.iteritems():
        if i == 5:
            break
        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]
            #print("http://" + url)
            resultURLs.append(url)
            #showSnippet(docID, positions)
            i += 1
    return resultURLs

# new for milestone 3
def query_index_better(input, index_dict, url_dict, totalDocuments):
    resultList = []
    scoring = {}

    query = re.sub(r'\W', ' ', input).lower().split()
    for q in query:
        if q in index_dict:
            # debugging purposes
            #print index_dict[q]
            resultList.append(index_dict[q])

    intersectKeys = set(resultList[0].keys())
    for r in resultList[1:]:
        intersectKeys |= set(r.keys())

    # debugging purposes
    #print resultList
    #print len(resultList)
    #print intersectKeys

    for q in query:
        for id in intersectKeys:
            if id in index_dict[q]:
                tf = math.log(1 + len(index_dict[q][id]))
                idf = math.log(totalDocuments / len(index_dict[q]))
                weight = tf * idf
                if id not in scoring:
                    scoring[id] = weight
                else:
                    scoring[id] += weight
                # debugging purposes
                # print q, id, tf, idf, weight
    scoring = sorted(scoring.items(), key = operator.itemgetter(1), reverse = True)

    # debugging purposes
    #print scoring
    #print resultList

    intersectDict = OrderedDict()
    # Take the top 5 weight score
    for j in range(5):
        key = scoring[j][0]
        intersectDict[key] = []
        for r in resultList:
            # debugging purposes
            #print r
            if key in r:
                # debugging purposes
                #print r[key]
                intersectDict[key].extend(r[key][0:2])
    # debugging purposes
    #print intersectDict

    i = 0
    resultURLs = []
    for key, positions in intersectDict.iteritems():
        if i == 5:
            break
        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]
            #print("http://" + url)
            resultURLs.append(url)
            #showSnippet(docID, positions)
            i += 1
    return resultURLs

# reference: https://www.kaggle.com/wendykan/ndcg-example
def getDCG5(r, k=5, method=1):
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.

def getNDCG5(DCGlist):
    #print DCGlist
    #print sorted(DCGlist, reverse=True)
    perfectDCG = getDCG5(sorted(DCGlist, reverse=True))
    if not perfectDCG:
        return 0.
    return getDCG5(DCGlist) / perfectDCG

path = 'webpages_clean/'
queries = [
    'mondego',
    'machine learning',
    'software engineering',
    'security',
    'student affairs',
    'graduate courses',
    'Crista Lopes',
    'REST',
    'computer games',
    'information retrieval'
]
totalDocuments = 37497
inverted_index = defaultdict(lambda: defaultdict(lambda: list()))
print "Opening json file, please wait..."
json_data = json.load(open('output.json'))
json_url_data = json.load(open(path + 'bookkeeping.json'))
googleResults = json.load(open('googleResults.json'))
i = 0
similarity_threshold = 0.9
for q in queries:
    Oracle = [re.sub('https://','', re.sub('http://', '', o)) for o in googleResults[i]]
    M2 = query_index(q, json_data, json_url_data)
    M3 = query_index_better(q, json_data, json_url_data, totalDocuments)

    pprint.pprint(queries[i])
    #pprint.pprint(Oracle)
    #pprint.pprint(M2)
    #pprint.pprint(M3)

    m2_DCG = []
    m3_DCG = []
    for j in range(0,5):
        o = Oracle[j]

        m2_best = 0
        for m in M2: m2_best = max(m2_best, SequenceMatcher(None, o, m).ratio())
        if m2_best >= similarity_threshold: m2_DCG.append(1)
        else: m2_DCG.append(0)

        m3_best = 0
        for m in M3: m3_best = max(m3_best, SequenceMatcher(None, o, m).ratio())
        if m3_best >= similarity_threshold: m3_DCG.append(1)
        else: m3_DCG.append(0)

    i += 1

    print('M2 NDCG@5', getNDCG5(m2_DCG))
    print('M3 NDCG@5', getNDCG5(m3_DCG))