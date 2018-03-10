from bs4 import BeautifulSoup
import os
import re
from collections import defaultdict
from collections import OrderedDict
import json

path = "webpages_clean/"

def create_index(a_dictionary, totalDocuments):
    w = open("monitoroutput.txt", 'w')
    for parentfilename in os.listdir(path):
        if os.path.isdir(path + parentfilename):
            #print "PARENT DIRECTORY: " + path + parentfilename
            w.write("PARENT DIRECTORY: " + path + parentfilename + "\n")
            for filename in os.listdir(path + parentfilename):
                if os.path.isfile(path + parentfilename + "/" + filename):
                    totalDocuments += 1
                    #print "\tSUB DIRECTORY: " + path + parentfilename + "/" + filename
                    w.write("\tSUB DIRECTORY: " + path + parentfilename + "/" + filename + "\n")
                    docID = parentfilename + "_" + filename
                    file = open((path + parentfilename + "/" + filename), "r")
                    cleantxtfile = BeautifulSoup(file, "lxml").text
                    line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
                    wordPos = 0
                    for word in line:
                        wordPos += 1
                        # Remove any word that contains number or special character
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
    w.close()
    # Added by Qiushi, to generate a json file of our index
    outputJSON(a_dictionary)
    outputBeautify(a_dictionary, totalDocuments)
    outputNormal(a_dictionary)
    print "Indexing done!"

def main():
    totalDocuments = 0
    inverted_index = defaultdict(lambda: defaultdict(lambda: list()))
    if not os.path.isfile("output.json"):
        print "Building an index, please wait..."
        create_index(inverted_index, totalDocuments)
    else:
        print "Opening json file, please wait..."
        json_data = json.load(open('output.json', 'r'))
        json_url_data = json.load(open(path + 'bookkeeping.json'))
        while True:
            input = raw_input("Search here: ")
            query_index(input, json_data, json_url_data)

def showSnippet(docID, positions):
    file = open((path + docID), "r")
    cleantxtfile = BeautifulSoup(file, "lxml").text
    line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
    eof = len(line)
    for p in positions:
        start = p-5 if p>=5 else 0
        end = p+5 if (p+5)<=eof else eof
        for i in range(start,end):
            print line[i].encode('ascii', 'ignore'),
        else:
            print
    return

# Scalable query index, could handle n-numbers of query
# Need to improve: the order of the query
def query_index(input, index_dict, url_dict):
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

    i = 0
    for key, positions in intersectDic.iteritems():
        if i == 5:
            break

        docID = key.replace('_', '/')
        if docID in url_dict:
            url = url_dict[docID]
            #print "DocID: " + str(docID) + ", URL: " + url
            print("http://"+url)
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

if __name__ == '__main__':
    main()