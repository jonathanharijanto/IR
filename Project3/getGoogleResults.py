# https://stackoverflow.com/questions/37754771/python-get-result-of-google-search
# https://developers.google.com/api-client-library/python/start/installation
# https://github.com/google/google-api-python-client/blob/master/samples/customsearch/main.py
# python -m pip install pip google-api-python-client

#import pprint
import json
from googleapiclient.discovery import build

# Kyungwoo Hyun's Google Account
# TEST URL: https://cse.google.com/cse/publicurl?cx=016664344819740721867:h_1vnsdwvoo
api_key = 'AIzaSyBqu3fD-SNVcUW_vuCgV38WJWgNDnlR1Bo'
cx = '016664344819740721867:h_1vnsdwvoo' #only in *.ics.uci.edu

def getTop(items,n):
    results = []
    i = 1
    for item in items:
        results.append(item['link'])

        if i == n: break
        else: i += 1

    return results


service = build("customsearch", "v1", developerKey=api_key)

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

googleResults = []
for q in queries:
    res = service.cse().list(q=q,cx=cx,).execute()
    items = res['items']
    res = service.cse().list(q=q,start=11,cx=cx,).execute()
    items.extend(res['items'])
    print len(items)
    googleResults.append(getTop(items,20))

with open('googleResults.json', 'w') as fp:
    json.dump(googleResults, fp)

