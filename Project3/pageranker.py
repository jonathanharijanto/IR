import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import re
import networkx as nx
import urllib2

path1 = 'webpages_clean/'
path2 = 'docs/'

regex = re.compile(r'\\(?![/u"])')

def preprocess():
    # 0) New a dictionary map <bookkeeping-file-id, index-0f-pagelinks>
    filemap = OrderedDict()

    # 1) Load the bookkeeping.json into dictionary
    print "Loading bookkeeping.json ..."
    bookkeeping = json.load(open(path1 + 'bookkeeping.json'))

    # 2) Load the pagelinks.json into dictionary
    print "Loading pagelinks.json ..."
    pagelinks = json.loads(regex.sub(r"\\\\", open('pagelinks.json').read()), object_pairs_hook=OrderedDict)

    # 3) Traverse bookkeeping: for each url
    #     3-1) look up the 'index' from pagelinks
    #     3-2) get the title from http request to the url
    #     3-3) write the title back to the value of the docID into bookkeeping
    #     3-4) write the index back to the filemap

    hits = 0
    progress = 0
    print "Traversing the bookkeeping ..."
    for filePath, url in bookkeeping.items():
        index = 0
        title = ''
        progress += 1
        if progress % 30 == 1:
            print "processed " + str(progress) + ", hits = " + str(hits)
        if 'http://' + url in pagelinks:
            index = pagelinks.keys().index('http://' + url)
            hits += 1
            try:
                soup = BeautifulSoup(urllib2.urlopen('http://' + url, timeout=10), 'lxml')
                title = soup.title.string
            except Exception as e:
                print e.message
        if not (title and title.strip()):
            title = filePath
        newval = {}
        newval['url'] = url
        newval['title'] = title
        bookkeeping[filePath] = newval

        filemap[filePath] = index


    print "Traversing finished.  hits = " + str(hits)

    # 4) Write back the bookkeepingNew.json
    print "Writing back the bookkeepingNew.json"
    with open(path1 + 'bookkeepingNew.json', 'w') as f:
       json.dump(bookkeeping, f)

    # 5) Write back the filemap.json
    print "Writing back the filemap.json"
    with open('filemap.json', 'w') as f:
        json.dump(filemap, f)


# def pagerank():
#     # 1) Generate the graph by replacing the urls by indexes
#     # 1-1) Load the pagelinks.json into dictionary
#     print "Loading pagelinks.json ..."
#     pagelinks = json.loads(regex.sub(r"\\\\", open('pagelinks.json').read()), object_pairs_hook=OrderedDict)
#
#     # 1-2) Traverse the pagelinks and replace each url with index and drop all urls not indexed
#     for vertex, edgelist in pagelinks.items():
#
#
#     # 2) Create networkx graph
#     G = nx.Graph()


if __name__ == '__main__':
    preprocess()