from bs4 import BeautifulSoup
import os
import re
from collections import Counter, defaultdict

path = "webpages_clean/"

os.getcwd()

global totalDocuments

def isValid(word):
    if word.isdigit():
        return False
    else:
        return True

def main():
    inverted_index = defaultdict(lambda: defaultdict(lambda: list()))
    word_count = {}
    w = open("monitoroutput.txt", 'w')
    global totalDocuments
    totalDocuments = 0
    for parentfilename in os.listdir(path):
        if os.path.isdir(path + parentfilename):
            print "parentdir: " + path + parentfilename
            w.write("PARENT DIRECTORY: " + path + parentfilename + "\n")
            for filename in os.listdir(path+parentfilename):
                if os.path.isfile(path + parentfilename + "/" + filename):
                    totalDocuments += 1
                    print "\tSUB DIRECTORY: " + path + parentfilename + "/" + filename
                    w.write("\tSUB DIRECTORY: " + path + parentfilename + "/" + filename + "\n")
                    docID = parentfilename + "_" + filename
                    file = open((path + parentfilename + "/" + filename), "r")
                    cleantxtfile = BeautifulSoup(file, "lxml").text
                    line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
                    wordPos = 0
                    for word in line:
                        wordPos += 1
                        if isValid(word):
                            word = word.encode('ascii', 'ignore')
                            if word in inverted_index:
                                if docID not in inverted_index[word]:
                                    inverted_index[word][docID] = list()
                                    inverted_index[word][docID].append(wordPos)
                                else:
                                    inverted_index[word][docID].append(wordPos)
                            else:
                                inverted_index[word][docID] = list()
                                inverted_index[word][docID].append(wordPos)

    w.close()
    outputBeautify(inverted_index)
    print "DONE!"

def outputBeautify(a_dictionary):
    w = open('outputfile.txt', 'w')
    w.write("Total unqiue words = " + str(len(a_dictionary.keys())) + "\n")
    w.write("Total documents = " + str(totalDocuments) + "\n")
    for i in a_dictionary:
        w.write(str(i) + " --> " )
        for j in a_dictionary[i]:
            w.write(str(j) + " ["+ str(a_dictionary[i][j])+"], ")
            #print str(i) + " --> " + str(a_dictionary[i]) + "\n"
        w.write("\n")
    w.close()

if __name__ == '__main__':
    main()