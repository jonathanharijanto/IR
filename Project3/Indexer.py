from bs4 import BeautifulSoup
import os
import re
from collections import defaultdict
from collections import OrderedDict
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import argparse
import math
import operator

path = "webpages_clean/"

def main():
    totalDocuments = 37497
    inverted_index = defaultdict(lambda: defaultdict(lambda: list()))
    if not os.path.isfile("output.json"):
        print "Building an index, please wait..."
        create_index(inverted_index, totalDocuments)
    else:
        print "Opening json file, please wait..."
        json_data = json.load(open('output.json', 'r'))
        json_url_data = json.load(open(path + 'bookkeepingNew.json'))
        while True:
            input = raw_input("Search here: ")
            query_index_better(input, json_data, json_url_data, totalDocuments)

def create_index(a_dictionary, totalDocuments):
    for parentfilename in os.listdir(path):
        if os.path.isdir(path + parentfilename):
            for filename in os.listdir(path + parentfilename):
                if os.path.isfile(path + parentfilename + "/" + filename):
                    totalDocuments += 1
                    docID = parentfilename + "_" + filename
                    file = open((path + parentfilename + "/" + filename), "r")
                    cleantxtfile = BeautifulSoup(file, "lxml").text
                    line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
                    wordPos = 0
                    for word in line:
                        wordPos += 1
                        if word.isalpha() == True:
                            word = word.encode('ascii', 'ignore')
                            if word in a_dictionary:
                                if docID not in a_dictionary[word]:
                                    a_dictionary[word][docID] = list()
                                    a_dictionary[word][docID].append(wordPos)
                                else:
                                    a_dictionary[word][docID].append(wordPos)
                            else:
                                a_dictionary[word][docID] = list()
                                a_dictionary[word][docID].append(wordPos)
    outputBeautify(a_dictionary, totalDocuments)
    outputNormal(a_dictionary)
    print "Indexing done!"

def showSnippet(docID, positions):
    file = open((path + docID), "r")
    cleantxtfile = BeautifulSoup(file, "lxml").text
    line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
    eof = len(line)
    positions = positions[::-2]
    for p in positions:
        start = p-5 if p >= 5 else 0
        end = p+5 if (p+5) <= eof else eof
        for i in range(start, end):
            print line[i].encode('ascii', 'ignore'),
        else:
            print
    return

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
    print resultList
    print len(resultList)
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
    print intersectDict

    i = 0
    for key, positions in intersectDict.iteritems():
        if i == 5:
            break
        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]['url']
            title = url_dict[docID]['title']
            print('------------------------------------------------------------------')
            print(title)
            print("http://" + url)
            showSnippet(docID, positions)
            i += 1

# old for milestone 2
def query_index(input, index_dict, url_dict):
    query = re.sub(r'\W', ' ', input).lower().split()
    resultList = []
    for q in query:
        if q in index_dict:
            resultList.append(index_dict[q])

    print resultList
    print len(resultList)
    intersectKeys = set(resultList[0].keys())
    print intersectKeys

    for r in resultList[1:]:
        intersectKeys &= set(r.keys())

    print intersectKeys

    intersectDict = OrderedDict()
    for key in intersectKeys:
        intersectDict[key] = []
        for r in resultList:
            if key in r:
                intersectDict[key].extend(sorted(r[key]))
    print intersectDict

    i = 0
    for key, positions in intersectDict.iteritems():
        if i == 5:
            break
        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]
            print("http://" + url)
            showSnippet(docID, positions)
            i += 1

def outputNormal(a_dictionary):
    with open('output.json', 'w') as fp:
        json.dump(a_dictionary, fp)

def outputBeautify(a_dictionary, totalDocuments):
    w = open('outputbeauty.txt', 'w')
    w.write("Total unique words = " + str(len(a_dictionary.keys())) + "\n")
    w.write("Total documents = " + str(totalDocuments) + "\n")
    for i in a_dictionary:
        w.write(str(i) + " --> ")
        for j in a_dictionary[i]:
            w.write(str(j) + " [" + str(a_dictionary[i][j]) + "], ")
        w.write("\n")
    w.write("Total size of index on disk: " + str(os.path.getsize('outputbeauty.txt')) + " bytes")
    w.close()

# Added by Qiushi, return Snippet for Http Service
def getSnippet(docID, positions):
    snippet = ''
    file = open((path + docID), "r")
    cleantxtfile = BeautifulSoup(file, "lxml").text
    line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
    eof = len(line)
    positions = positions[::-2]
    for p in positions:
        start = p-5 if p >= 5 else 0
        end = p+5 if (p+5) <= eof else eof
        for i in range(start, end):
            snippet += str(line[i].encode('ascii', 'ignore')) + ' <br> '
    return snippet

# Added by Qiushi
# new for milestone 3
def query_index_better_rest(input, index_dict, url_dict, totalDocuments):
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
    print resultList
    print len(resultList)
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
    print intersectDict

    resultJSON = '[\n'

    i = 0
    for key, positions in intersectDict.iteritems():
        if i == 5:
            break
        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]['url']
            title = url_dict[docID]['title']
            fullUrl = 'http://' + url
            description = getSnippet(docID, positions)
            if i > 0:
                resultJSON += ',\n'
            resultJSON += '{'
            resultJSON += '\"title\": \"' + title + '\",'
            resultJSON += '\"url\": \"' + fullUrl + '\",'
            resultJSON += '\"description\": \"' + description + '\"'
            resultJSON += '}'
            i += 1

    resultJSON += '\n]'
    return resultJSON

# Added by Qiushi, query index for Http Service, return JSON
def query_index_rest(input, index_dict, url_dict):
    query = re.sub(r'\W', ' ', input).lower().split()
    resultList = []
    for q in query:
        if q in index_dict:
            resultList.append(index_dict[q])

    intersectKeys = set(resultList[0].keys())
    for r in resultList[1:]:
        intersectKeys &= set(r.keys())

    intersectDic = OrderedDict()
    for key in intersectKeys:
        for r in resultList:
            intersectDic[key] = r[key]

    resultJSON = '[\n'

    i = 0
    for key, positions in intersectDic.iteritems():
        if i == 5:
            break

        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]['url']
            title = url_dict[docID]['title']
            fullUrl = 'http://' + url
            description = getSnippet(docID, positions)
            if i > 0:
                resultJSON += ',\n'
            resultJSON += '{'
            resultJSON += '\"title\": \"' + title + '\",'
            resultJSON += '\"url\": \"' + fullUrl + '\",'
            resultJSON += '\"description\": \"' + description + '\"'
            resultJSON += '}'
            i += 1

    resultJSON += '\n]'
    return resultJSON

# Added bushi, for generate a json file of our index
def outputJSON(a_dictionary):
    w = open('index.json', 'w')
    w.write("{\n")
    c1 = 0
    for i in a_dictionary:
        if c1 > 0:
            w.write(",")
        w.write("\"" + str(i) + "\": ")
        w.write("{")
        c2 = 0
        for j in a_dictionary[i]:
            if c2 > 0:
                w.write(", ")
            w.write("\"" + str(j) + "\": " + str(a_dictionary[i][j]))
            c2 += 1
        w.write("}\n")
        c1 += 1
    w.write("}")
    w.close()


# Added by Qiushi, for load a json file into dict
def loadJSON():
    import json
    from pprint import pprint

    inverted_index = json.load(open('index.json'))

    pprint(inverted_index["fawn"])


# Added by Qiushi, for handle http request
class HttpService(BaseHTTPRequestHandler):

    def __init__(self, jsonData, jsonUrlData, query, *args):
        self.json_data = jsonData
        self.json_url_data = jsonUrlData
        self.query = query
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        totalDocuments = 37497
        self._set_headers()
        import urlparse
        o = urlparse.urlparse(self.path)
        q = urlparse.parse_qs(o.query)
        print q
        input = q['search'].pop()
        print "search = " + input

        if self.query == 'o' or self.query == 'old' or self.query == 'O' or self.query == 'OLD':
            resultJSON = query_index_rest(input, self.json_data, self.json_url_data)
        else:
            resultJSON = query_index_better_rest(input, self.json_data, self.json_url_data, totalDocuments)

        print "result = " + resultJSON

        self.wfile.write(resultJSON)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,HEAD,OPTIONS,POST,PUT')
        self.send_header('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
        self.end_headers()


# Added by Qiushi, entrance function for http server
def run(server_class=HTTPServer, handler_class=HttpService, port=8088, query='new'):
    inverted_index = defaultdict(lambda: defaultdict(lambda: list()))

    print 'Starting httpd...'
    if not os.path.isfile("output.json"):
        print "Building inverted index..."
        create_index(inverted_index, totalDocuments)
        print "Building finished."

    print "Loading output.json..."
    json_data = json.load(open('output.json', 'r'))
    print "Loading bookkeeping.json..."
    json_url_data = json.load(open(path + 'bookkeepingNew.json'))
    print "Loading finished."

    server_address = ('', port)

    def handler(*args):
        handler_class(json_data, json_url_data, query, *args)
    httpd = server_class(server_address, handler)
    print "Web server started!"
    httpd.serve_forever()


# Modified by Qiushi, use parameters to start http server.
# python Indexer.py --help
# python Indexer.py -m server
# python Indexer.py -m server -p 8081
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mode', help='mode [s]erver or [t]erminal, default terminal')
    parser.add_argument(
        '-p', '--port', type=int, help='point (only valid when -m is server)')
    parser.add_argument(
        '-q', '--query', help='query [o]ld or [n]ew, default new')

    args = parser.parse_args()

    if args.mode == 's' or args.mode == 'server' or args.mode == 'S' or args.mode == 'SERVER':
        if args.port:
            run(port=int(args.port), query=args.query)
        else:
            run(query=args.query)
    else:
        main()
