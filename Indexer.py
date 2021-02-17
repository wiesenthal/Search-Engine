import os
import json
from bs4 import BeautifulSoup
import PartA

# <token, posting_list>
# posting [docID, tf-idf_score *Frequency for now*, ...]
# should probably sort by docID in the posting list



class Index:
    def __init__(self, start_path):
        self.start_path = start_path
        self.index = {}
        self.lastUsedIndex = 0
        self.url_list = {}
        self.num_sites = 0
        self.doc_list = self.getDocuments()
        self.total_sites = len(self.doc_list)
        self.current_batch = 1

        self.index_path = "indexes/index" #  the path to be added before index names

    def assignUrlID(self, url):
        return len(self.url_list)

    # gets all the document paths
    def getDocuments(self):
        doc_list = []
        for root, dirs, files in os.walk(self.start_path):
            for file in files:
                doc_list.append(os.path.join(root, file))
                self.num_sites += 1
        return doc_list

    # write the current index to the disk and empty it
    def writeToDisk(self):
        file_name = self.index_path + str(self.current_batch) + ".txt"
        self.current_batch += 1
        partial_index = open(file_name, "w")
        for word in sorted(self.index):
            temp_dict = {word: self.index[word]}
            partial_index.write(json.dumps(temp_dict)+"\n")

    def writeUrlList(self):
        urlMap = open("urlMap.txt", "w")
        for siteID in self.url_list:
            temp_dict = {siteID: self.url_list[siteID]}
            urlMap.write(json.dumps(temp_dict) + "\n")

    # builds the index/map from the provided folder containing the json files
    def buildIndex(self):
        batch1 = int(self.total_sites/3)
        batch2 = int(2*self.total_sites/3)
        siteID = 0
        for file in self.doc_list:
            # write to disk on each batch and empty the current index
            if siteID == batch1 or siteID == batch2:
                self.writeToDisk()
                self.index = {}
            with open(file, "r") as auto:
                site = json.load(auto)
                # Json format is site, content, encoding
                # print(file)
                # print("------------------------------------------\n")
                # print("site: ", site['url'])
                # print("encoding: ", site['encoding'])
                # print("content: ", site['content'])
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
        self.writeToDisk()
        self.writeUrlList()


def main():
    ind = Index('DEV')
    ind.buildIndex()
    #for word in ind.index:
    #    print(word, " - ", ind.index[word])
    # {"url": "https://aiclub.ics.uci.edu/",
    print("number of sites: ", ind.num_sites)
    print("number of unique tokens: ", len(ind.index))


if __name__ == '__main__':
    main()