import sys
import fileinput
import json


class SearchInterface:

    # TODO searches the index for the given terms and returns best matches
    def matchingDocuments(self, terms, index):
        docs = []
        return docs

    # merge the partial indexes
    # should probably put this and its utilities in its on class/file
    def mergeIndexes(self, *index_filenames):

        output_file = open("all_index.txt", 'w')  # output file to write to

        index_files = []  # the opened index files
        file_pos = []  # the current positions of those indexes corresponding to array index (might be unnecessary)
        cur_lines = []  # the current lines of those indexes corresponding to array index
        cur_data = []  # the current json data of those indexes corresponding to array index
        # fill the above arrays, allowing dynamic number of indexes
        for filename in index_filenames:
            f = open(filename, "r")
            index_files.append(f)

            # get the cur_lines started
            file_pos.append(f.tell())
            cur_lines.append(f.readline())

        while any(index_files):  # while any of the files have content left
            min_word = ""  # the first word lexicographically for the final index
            min_index = -1
            # go through all the indexes, getting the lines and keeping track of file positions
            for i in range(len(index_files)):

                if cur_lines[i]:  # only add to data if there is content in the line
                    cur_data[i] = json.loads(cur_lines[i])
                    key_word = list(cur_data[i].keys())[0]  # this gives us the word that we want
                    if not min_word or key_word < min_word:
                        min_word = key_word
                        min_index = i
                else:
                    cur_data[i] = None

            if min_index == -1 and not min_word:  # if the line was blank
                break

            # write min word to output file
            output_file.write(cur_data[min_index])
            # read new line from the index that was used
            file_pos[min_index] = index_files[min_index].tell()
            cur_lines[min_index] = index_files[min_index].readline()

        # close the files
        for file in index_files:
            file.close()
        output_file.close()

    # gets the search query from the commandline
    def getQuery(self):
        argsc = len(sys.argv)
        query = []  # list of terms from the given query
        for arg in sys.argv:
            query.append(arg)
        for term in query:
            print(term)
        return query


def main():
    interface = SearchInterface()
    print(interface.getQuery())
    interface.mergeIndexes()


if __name__ == '__main__':
    main()
