import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import re

path1 = 'webpages_clean/'
path2 = 'docs/'

regex = re.compile(r'\\(?![/u"])')

def main():
    # 1) Load the bookkeeping.json into dictionary
    print "Loading bookkeeping.json ..."
    bookkeeping = json.load(open(path1 + 'bookkeeping.json'))

    # 2) Load the pagelinks.json into dictionary
    print "Loading pagelinks.json ..."
    pagelinks = json.loads(regex.sub(r"\\\\", open('pagelinks.json').read()), object_pairs_hook=OrderedDict)

    # 3) Traverse bookkeeping and look up the original html file 'index' from pagelinks:
    #     3-1) read the 'index'.txt file
    #     3-2) find the title of this document
    #     3-3) write the title back to the value of the docID into bookkeeping
    hits = 0
    progress = 0
    print "Traversing the bookkeeping ..."
    for filePath, url in bookkeeping.items():
        title = ''
        progress += 1
        if progress % 30 == 1:
            print "processed " + str(progress) + ", hits = " + str(hits)
        if 'http://' + url in pagelinks:
            index = pagelinks.keys().index('http://' + url)
            hits += 1
            try:
                doc = open(path2 + str(index) + '.txt')
                soup = BeautifulSoup(doc.read(), "lxml")
                title = soup.title.string
            except Exception as e:
                print e.message
        if not (title and title.strip()):
            title = filePath
        newval = {}
        newval['url'] = url
        newval['title'] = title
        bookkeeping[filePath] = newval

    print "Traversing finished.  hits = " + str(hits)

    # 4) Write back the bookkeepingNew.json
    print "Writing back the bookkeepingNew.json"
    with open(path1 + 'bookkeepingNew.json', 'w') as f:
        json.dump(bookkeeping, f)


if __name__ == '__main__':
    main()