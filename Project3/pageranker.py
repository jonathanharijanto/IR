import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import re
#import networkx as nx
import urllib2
import datetime
import time
from urlparse import urlparse

path1 = 'webpages_clean/'
path2 = 'docs/'

regex = re.compile(r'\\(?![/u"])')


def add_prs():
    # 0) New a dictionary map <bookkeeping-file-id, pr>
    prmap = OrderedDict()

    # 1) Load the bookkeeping.json into dictionary
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Loading bookkeeping.json ..."
    bookkeeping = json.load(open(path1 + 'bookkeeping.json'))

    # 2) Load the pr.json into dictionary
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Loading pr.json ..."
    pr = json.load(open('pr.json'))

    # 3) Load the pagelinks.json into dictionary
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Loading pagelinks.json ..."
    pagelinks = json.loads(regex.sub(r"\\\\", open('pagelinks.json').read()), object_pairs_hook=OrderedDict)

    # 4) Traverse bookkeeping: for each url
    #    look up the 'index' from pagelinks
    #    look up the pr value from pr
    #    write back to the prmap
    hits = 0
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Traversing the bookkeeping ..."
    for filePath, url in bookkeeping.items():
        if 'http://' + url in pagelinks:
            index = pagelinks.keys().index('http://' + url)
            hits += 1
            prmap[filePath] = pr[str(index)]


    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Traversing finished.  hits = " + str(hits)

    # 5) Write back the prmap.json
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Writing back the prmap.json"
    with open('prmap.json', 'w') as f:
        json.dump(prmap, f)


def is_valid(url):

    result = False

    # Get original url string
    if type(url) == str:
        # Ignore errors even if the string is not proper UTF-8 or has
        # broken marker bytes.
        # Python built-in function unicode() can do this.
        original = unicode(url, "utf-8", errors="ignore")
    else:
        # Assume the value object has proper __unicode__() method
        original = unicode(url)

    parsed = urlparse(url)

    # print "Validating url: [", original, "]"
    # print "Parsed url: ", str(parsed)
    # try:
        # logging.info("Validating url: [" + original + "]")
        # logging.info("Parsed url: " + parsed)
    # except TypeError:
    #    print ("TypeError for logging: ", TypeError.message)

    if parsed.scheme not in set(["http", "https"]):

        result = False

        return result

    try:
        result = ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z"
                + "|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv"
                + "|rm|smil|wmv|swf|wma|zip|rar|gz|txt|datasets)$", parsed.path.lower())\
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z"
                + "|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv"
                + "|rm|smil|wmv|swf|wma|zip|rar|gz|txt|datasets)$", original.lower())\
            and not re.match("^.*calendar.*$", parsed.path.lower()) \
            and not re.match("^.*calendar.*$", original.lower()) \
            and not re.match("^.*/[^/]{10,}$", parsed.path) \
            and not re.match("^.*/[^/]{10,}$", original) \
            and not re.match("^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path.lower())\
            and not re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme|/datasets|/dataset){3}.*$", parsed.path.lower())

        return result

    except TypeError:
        return False
    except Exception as e:
        return False


def add_titles():
    # 1) Load the bookkeeping.json into dictionary
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Loading bookkeeping.json ..."
    bookkeeping = json.load(open(path1 + 'bookkeeping.json'))

    # 3) Traverse bookkeeping: for each url
    #     3-1) get the title from http request to the url
    #     3-2) write the title back to the value of the docID into bookkeeping
    progress = 0
    titles = 0
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Traversing the bookkeeping ..."
    for filePath, url in bookkeeping.items():
        title = ''

        if progress % 30 == 1:
            print "processed " + str(progress) + ", titles = " + str(titles)

        if is_valid('http://' + url):
            try:
                soup = BeautifulSoup(urllib2.urlopen('http://' + url, timeout=3), 'lxml')
                title = soup.title.string
            except Exception as e:
                print "loading http://" + url
                print "error: " + e.message

        if not (title and title.strip()):
            title = filePath
        else:
            titles += 1

        newval = {}
        newval['url'] = url
        newval['title'] = title
        bookkeeping[filePath] = newval

        progress += 1

    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Traversing finished.  titles = " + str(titles)

    # 4) Write back the bookkeepingNew.json
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Writing back the bookkeepingNew.json"
    with open(path1 + 'bookkeepingNew.json', 'w') as f:
       json.dump(bookkeeping, f)


'''
def start_pr():
    # 1) Generate the graph by replacing the urls by indexes
    # 1-1) Load the pagelinks.json into dictionary
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "1-1) Loading pagelinks.json ..."
    pagelinks = json.loads(regex.sub(r"\\\\", open('pagelinks.json').read()), object_pairs_hook=OrderedDict)

    # 1-2) Traverse the pagelinks and replace each edge url with index and drop all urls not indexed
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "1-2) Traverse the pagelinks and replace each edge url with index and drop all urls not indexed..."
    for vertex, edgelist in pagelinks.items():
        newedgelist = []
        for edge in edgelist:
            if edge in pagelinks:
                v = pagelinks.keys().index(edge)
                newedgelist.append(v)
        pagelinks[vertex] = newedgelist

    # 1-3) Traverse the pagelinks and replace each vertex url with index
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "1-3) Traverse the pagelinks and replace each vertex url with index..."
    for index, (vertex, edgelist) in enumerate(pagelinks.items()):
        pagelinks[index] = pagelinks.pop(vertex)

    # 2) Create networkx graph
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "2) Create networkx graph..."
    G = nx.Graph()
    for v, es in pagelinks.items():
        G.add_node(v)
        for e in es:
            G.add_edge(v, e)

    # 3) Calculate pagerank values:
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "3) Calculate pagerank values..."
    pr = nx.pagerank(G)

    # 4) Write back the pr values into pr.json
    print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "Writing back the pr.json"
    with open('pr.json', 'w') as f:
        json.dump(pr, f)
'''

if __name__ == '__main__':
    # start_pr()
    # print "nothing happens."
    add_titles()
    # add_prs()
