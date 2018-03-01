from bs4 import BeautifulSoup
import os
import re

path = "../WEBPAGES_CLEAN/"

os.getcwd()

def main():
    inverted_index = {}
    word_count = {}
    w = open("monitor.txt", w)
    for parentfilename in os.listdir(path):
        print "parentdir: " + parentfilename, path+parentfilename
        w.write("PARENT DIRECTORY: " + parentfilename, path+parentfilename)
        for filename in os.listdir(path+parentfilename):
            print "\tSUB DIRECTORY: " + filename, path + parentfilename + "/" + filename
            docID = parentfilename + filename
            file = open((path + parentfilename + "/" + filename), "r")
            cleantxtfile = BeautifulSoup(file, "lxml").text
            line = re.sub(r'\W', ' ', cleantxtfile).lower().split()
            for word in line:
                word = word.encode('ascii', 'ignore')
                if word in inverted_index:
                    if docID not in inverted_index[word]:
                        inverted_index.setdefault(word, []).append(docID)
                else:
                    inverted_index.setdefault(word, []).append(docID)
    w.close()
    outputBeautify(inverted_index)

def outputBeautify(a_dictionary):
    w = open('outputfile.txt', 'w')
    for i in a_dictionary:
        #print str(i) + " --> " + str(a_dictionary[i]) + "\n"
        w.write(str(i) + " --> " + str(a_dictionary[i]) + "\n")
    w.close()

if __name__ == '__main__':
    main()