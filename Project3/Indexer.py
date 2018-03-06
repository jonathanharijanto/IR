from bs4 import BeautifulSoup
import os
import re
from collections import Counter, defaultdict

path = "webpages_clean/"

# Unused function
def isValid(word):
    if word.isdigit():
        return False
    else:
        return True

def weighting():
    print "haha"
    # term frequency = ?
    # tf_score = log( 1 + tf) -- base 10
    # document frequency = ?
    # df_score = log( N / df ) -- base 10
    # tf-idf weight = tf_score * df_score

def doc_score():
    print "hehe"
    # score(query,document) = sum_of_all(tf * idf)

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
    print "DONE!"

def main():
    totalDocuments = 0
    inverted_index = defaultdict(lambda: defaultdict(lambda: list()))
    create_index(inverted_index, totalDocuments)
    query = raw_input("Search here: ")
    # First condition: single query -- go to dictionary and retrieve the docs
    if len(query.split()) == 1:
        if query in inverted_index:
            for doc in inverted_index[query]:
                # Split the input XX_XXX into XX(parent folder) & XXX(folder)
                doc = re.sub("_", " ", doc).split()
                print "URL: " + path + doc[0] + "/" + doc[1]
    # Second condition: not a single query -- do scoring and retrieve the docs
    else:
        print "happy happy"
    # Added by Qiushi, if you want to load the JSON file or index, call loadJSON()
    # loadJSON()


def outputBeautify(a_dictionary, totalDocuments):
    w = open('outputfile.txt', 'w')
    w.write("Total unique words = " + str(len(a_dictionary.keys())) + "\n")
    w.write("Total documents = " + str(totalDocuments) + "\n")
    for i in a_dictionary:
        w.write(str(i) + " --> ")
        for j in a_dictionary[i]:
            w.write(str(j) + " [" + str(a_dictionary[i][j]) + "], ")
            #print str(i) + " --> " + str(a_dictionary[i]) + "\n"
        #w.write("\t" + str(len(a_dictionary[i])))
        w.write("\n")
    w.write("Total size of index on disk: " + str(os.path.getsize('outputfile.txt')) + " bytes")
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