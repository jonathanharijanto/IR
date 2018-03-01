from bs4 import BeautifulSoup
import os
import re

path = "webpages_clean/"

os.getcwd()

def main():
    inverted_index = {}
    word_count = {}
    w = open("monitoroutput.txt", 'w')
    for parentfilename in os.listdir(path):
        print "parentdir: " + path + parentfilename
        w.write("PARENT DIRECTORY: " + path + parentfilename + "\n")
        for filename in os.listdir(path+parentfilename):
            print "\tSUB DIRECTORY: " + path + parentfilename + "/" + filename
            w.write("\tSUB DIRECTORY: " + path + parentfilename + "/" + filename + "\n")
            docID = parentfilename + "_" + filename
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
    print "DONE!"

def outputBeautify(a_dictionary):
    w = open('outputfile.txt', 'w')
    for i in a_dictionary:
        #print str(i) + " --> " + str(a_dictionary[i]) + "\n"
        w.write(str(i) + " --> " + str(a_dictionary[i]) + "\n")
    w.close()

if __name__ == '__main__':
    main()