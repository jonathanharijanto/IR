from bs4 import BeautifulSoup
import os
import re
from collections import defaultdict
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
        input = raw_input("Search here: ")
        query = input.split()
        # One-word query
        if len(query) == 1:
            docID = None
            max_freq = None
            for id in json_data[query[0]]:
                print id, len(json_data[query[0]][id])
                if len(json_data[query[0]][id]) > max_freq:
                    max_freq = len(json_data[query[0]][id])
                    docID = id
            print "The Highest Freq: " + str(docID) + " " + str(max_freq)
            docID = docID.replace('_', '/')
            if docID in json_url_data:
                url = json_url_data[docID]
                print "DocID: " + str(docID) + ", URL: " + url
        # More-than-one-word query
        # Note to self: still need a better approach
        elif len(query) == 2:
            list_1 = []
            list_2 = []
            for id in json_data[query[0]]:
                list_1.append(id.encode('ascii', 'ignore'))
            for id in json_data[query[1]]:
                list_2.append(id.encode('ascii', 'ignore'))
            docID = list(set(list_1).intersection(set(list_2)))
            print docID
            docID = docID[0].replace('_', '/')
            if docID in json_url_data:
                url = json_url_data[docID]
                print "DocID: " + str(docID) + ", URL: " + url
    # Added by Qiushi, if you want to load the JSON file or index, call loadJSON()
    # loadJSON()

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

# Added by Qiushi, for generate a json file of our index
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