# https://stackoverflow.com/questions/37754771/python-get-result-of-google-search
# https://developers.google.com/api-client-library/python/start/installation
# https://github.com/google/google-api-python-client/blob/master/samples/customsearch/main.py
# python -m pip install pip google-api-python-client

#import pprint
from googleapiclient.discovery import build

# Kyungwoo Hyun's Google Account
api_key = 'AIzaSyBqu3fD-SNVcUW_vuCgV38WJWgNDnlR1Bo'
cx = '016664344819740721867:h_1vnsdwvoo' #only in *.ics.uci.edu

service = build("customsearch", "v1", developerKey=api_key)
res = service.cse().list(q='machine learning',cx=cx,).execute()
#pprint.pprint(res)
items = res['items']

i = 1
for item in items:
    print i, item['link']
    print item['snippet']

    if i == 5: break
    else: i += 1



