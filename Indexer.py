import os
import json
from bs4 import BeautifulSoup
import PartA

# <token, posting_list>
# posting [docID, tf-idf_score *Frequency for now*, ...]
# should probably sort by docID in the posting list



# checks if a URL has been assigned an ID number, if it has return that number else return
# a new unused int ID
class Index:
    def __init__(self, start_path):
        self.start_path = start_path
        self.index = {}
        self.lastUsedIndex = 0
        self.url_list = {}

    def assignUrlID(self, url):
        return len(self.url_list)

    # gets all the document paths
    def getDocuments(self):
        doc_list = []
        for root, dirs, files in os.walk(self.start_path):
            for file in files:
                doc_list.append(os.path.join(root, file))
        return doc_list

    # builds the index/map from the provided folder containing the json files
    def buildIndex(self):
        doc_list = self.getDocuments()
        for file in doc_list:
            with open(file, "r") as auto:
                site = json.load(auto)
                # Json format is site, content, encoding
                # print(file)
                # print("------------------------------------------\n")
                # print("site: ", site['url'])
                # print("encoding: ", site['encoding'])
                # print("content: ", site['content'])
                # tokenize the words
                # add tokens to index if they arent already
                # add a posting for that document to the posting List of the token (sort by ID?)
                siteID = self.assignUrlID(site['url'])
                # if url_list.get(siteID):
                #    continue

                soup = BeautifulSoup(site['content'], "lxml")
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                visible_text = soup.getText()
                # print(visible_text)
                token_list = PartA.tokenize(visible_text)
                temp_map = PartA.computeWordFrequencies(token_list)
                self.url_list[siteID] = site['url']
                for word in temp_map:
                    temp_tuple = [siteID, temp_map[word]]
                    if word in self.index:
                        self.index[word].append(temp_tuple)
                    else:
                        self.index[word] = []
                        self.index[word].append(temp_tuple)
        return


def main():
    ind = Index('DEV')
    ind.buildIndex()
    for word in ind.index:
        print(word, " - ", ind.index[word])


if __name__ == '__main__':
    main()
