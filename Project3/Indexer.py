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
    outputBeautify(a_dictionary, totalDocuments)
    outputNormal(a_dictionary)
    print "DONE!"

def main():
    totalDocuments = 0
    inverted_index = defaultdict(lambda: defaultdict(lambda: list()))
    #if not os.path.isfile("output.txt"):
    create_index(inverted_index, totalDocuments)
    input = raw_input("Search here: ")
    query = input.split()
    # First condition: single query -- go to dictionary and retrieve the docs
    if len(query) == 1:
        docID = None
        max_freq = None
        for id in inverted_index[query]:
            print id, len(inverted_index[query][id])
            if len(inverted_index[query][id]) > max_freq:
                max_freq = len(inverted_index[query][id])
                docID = id
        print docID, max_freq
        docID = docID.replace('_', '/')
        print docID
        json_data = json.load(open(path + 'bookkeeping.json'))
        if docID in json_data:
            url = json_data[docID]
            print docID, url
    # Second condition: not a single query -- do scoring and retrieve the docs
    elif len(query) == 2:
        list_1 = []
        list_2 = []
        for id in inverted_index[query[0]]:
            list_1.append(id)
        for id in inverted_index[query[1]]:
            list_2.append(id)
        docID = set(list_1).intersection(set(list_2))
        print docID

def outputNormal(a_dictionary):
    f = open("output.txt", "w")
    f.write(str(a_dictionary))
    f.close()

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

if __name__ == '__main__':
    main()