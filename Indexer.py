import os
import json
from bs4 import BeautifulSoup



# <token, posting_list>
# posting [docID, tf-idf_score *Frequency for now*, ...]
# should probably sort by docID in the posting list
index = {}


# checks if a URL has been assigned an ID number, if it has return that number else return
# a new unused int ID
def assignUrlID(url):
    return


# use partA probably
def wordFrequency():
    return

#builds the index/map from the provided folder containing the json files
def buildIndex():
    for root, dirs, files in os.walk('DEV'):
        for file in files:
            with open(os.path.join(root, file), "r") as auto:
                site = json.load(auto)
                # Json format is site, content, encoding
                #print(auto)
                #print("------------------------------------------\n")
                #print("site: ", site['url'])
                #print("encoding: ", site['encoding'])
                #print("content: ", site['content'])
                # tokenize the words
                # add tokens to index if they arent already
                # add a posting for that document to the posting List of the token (sort by ID?)



    return


def main():
    buildIndex()


if __name__ == '__main__':
    main()
