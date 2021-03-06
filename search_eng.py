"""Module containing classes ContextWindow and SearchEngine.

SearchEngine contains methods for searching the words within the database and
finding their context windows.
"""


from tokenizer_gen import Tokenizer
from f_indexator import Position_d
import shelve
import re
from sorting import our_sort
from morphan import Stemmer_agent


class ContextWindow(object):
    """Class of Context Windows.

    methods:
    get_bold -- add bold tags to the center of the CW
    extend_cw -- extend CW to a sentence
    """
    def __init__(self, pos, line, ext):
        self.pos = pos
        self.line = line
        self.ext = ext
        # tokenize the line
        ws = list(Tokenizer().alph_tokenize(line))
        for n, word in enumerate(ws):
            # set right border of the context window
            if word.f_ch == pos[0].start:
                if n - ext >= 0:
                    self.left = ws[n - ext].f_ch
                else:
                    self.left = 0
                # set right border of the context window
            if word.l_ch == pos[-1].end:
                try:
                    self.right = ws[n + ext].l_ch
                except IndexError:
                    self.right = len(line)-1

    def get_bold(self, line):
        """Enclose the center of the contex window in bold tags.

        The center is defined as a word/words positions of which are a pos parameter of CW
        Bold tag is a html tag: <b>center_word</b>

        :return: input line with bold tags
        :param line: input line
        """
        for n, p in enumerate(self.pos):
            line = line[:p.start+7*n]+"<b>"+line[p.start+7*n:p.end+7*n+1]+"</b>"+line[p.end+7*n+1:]
        return line       

    def extend_cw(self, line):
        """Extend CW to the borders of the sentense.

        :return: start and end indices of the extended CW
        :param line: input line
        """
        sent_end = '[.?!] [A-ZА-Я0-9]'
        try:
            new_end = list(re.finditer(sent_end, line[self.right+1:]))[0].start() + self.right + 1
        # if the line doesn't contain the end of the sentence
        except IndexError:
            new_end = len(self.line) - 1
        try:
            new_start = list(re.finditer(sent_end, line[:self.left+1]))[-1].end() - 1
        # if the line doesn't contain the beginning of the sentence 
        except IndexError:
            new_start = 0
        return new_start, new_end
        
    def __eq__(self, other):
        return ((self.pos[i] == other.pos[i] for i in range(len(self.pos)-1)) and (self.line == other.line)
                and (self.ext == other.ext))

    def __repr__(self):
        return self.line[self.left:self.right+1]


class SearchEngine(object):
    """Class that performs search in a database.

    Methods:
    ultimate_out -- return sentenses or context window of positions in files
    combine_cw -- combine overlapping context windows 
    get_context_w -- return n adjasent words to the left and right of the position in file
    get_word -- return word from a position in file
    search -- return a dictionary of files and positions of a word
    search_mult -- return a dictionary of files and positions of an each word in the query
    """
    def __init__(self, db):
        self.db = shelve.open(db)

    def __del__(self):
        self.db.close()

    def ultimate_out(self, files, mass):
        """Extend CWs where necessary and put in bold center words.

        :return: dictionary of filenames and extended CWs
        :param files: dictionary of filenames and CWs
        """
        self.files = files  # dictionary file:list of context windows
        #print(files)
        for f in files:
            cws = files[f]
            files[f] = self.gen_extended(cws)
        for f in files:
            cws = list(files[f])
            files[f] = self.gen_combined_cw(cws)
        #for fi in files:
         #   print(fi, list(files[fi]))
        for m, f in enumerate(sorted(files)):
            cws = list(files[f])
            #print(m, cws)
            files[f] = self.gen_bold(mass[m], cws, mass)
        return files

    def gen_extended(self, cws):
        for i in cws:
            new = i.extend_cw(i.line)
            i.left = new[0]
            i.right = new[-1]+1
            yield i

    def gen_bold(self, m, cws, mass):
        for n, i in enumerate(cws):
            if n >= m[0] and n < (m[0] + m[1]):
                yield i.get_bold(i.line)[i.left:i.right+7*len(i.pos)]

    def combine_cw(self, files):        
        """Combine overlapping context window.

        Overlapping context windows are two adjecent windows
        where the left border of one is between the left and right borders of another.

        :return: dictionary of filenames and combined (if necessary) context windows
        :param files: dictionary of files and context windows
        """
        self.files = files  # dictionary of files and context windows
        for f in files:
            cws = list(files[f])
            files[f] = self.gen_combined_cw(cws)
        return files
                
    def gen_combined_cw(self, cws):
        for i, cont in enumerate(cws):
                try:
                    if cont.line == cws[i+1].line and cws[i+1].left <= cont.right:
                        for npos in cws[i+1].pos:
                            cont.pos.append(npos)
                        cont.right = cws[i+1].right
                        yield cont
                        del cws[i+1]
                        #print(cont.pos)
                    else:
                        yield cont
                except IndexError:
                    break

    def get_context_w(self, files, ext):
        """Get context widwow for each file and each position in file.

        Open file and iterate its lines.
        Iterate list of positions
        When the number of line is equal to the position's number of line, create ContextWindow object.

        :return: dictionary of filenames and ContextWindow object for each position in that file
        :param files: dictioanry of filenames and Positions_d in those files
               ext: the width of the context window
        """
        self.files = files  # dictionary of files and positions
        self.ext = ext
        res = {}
        for f in files:
            posit = files[f]
            res[f] = self.gen_context_w(f, posit, ext)
        return res

    def gen_context_w(self, f, positions, ext):
        with open(f, 'r', encoding="utf-8") as file:
            it1 = enumerate(file)  # file iterator
            it2 = iter(positions)  # positions iterator
            cur_numl, cur_line = next(it1)
            cur_pos = next(it2)
            while True:
                # print(cur_numl, cur_line, cur_pos)
                if cur_numl < cur_pos.line:
                    try:
                        cur_numl, cur_line = next(it1)
                    except StopIteration:
                        break
                elif cur_numl > cur_pos.line:
                    try:
                        cur_pos = next(it2)
                    except StopIteration:
                        break
                else:
                    yield ContextWindow([cur_pos], cur_line, ext)
                    try:
                        cur_pos = next(it2)
                    except StopIteration:
                        break

    def get_word(self, f, pos):
        """Get substring from position in file.

        :return: word at the input position in the file
        :param f: filename
               pos: input Position_d object
        """
        self.pos = pos
        self.f = f
        with open(f, 'r', encoding="utf-8") as file:
            for i, line in enumerate(file):
                if i == pos.line:
                    return line[pos.start:pos.end+1]
                     
    def search(self, word, limit, offset):
        """One word search.

        :return: list of positions of the word in the database
        :param db: database containing file(s)
               word: input query word
        """
        self.word = word
        res = {}
        output = {}
        dic = self.db 
        res = dic.get(word, default=[])
        keys = sorted(list(res.keys()))
        for num, k in enumerate(keys):
            if num >= offset and num < (offset + limit):
                for el in output:
                    our_sort(output[el])
        return output

    def search_mult(self, query, limit, offset):
        """Multiword search.

        :return: a dictionary with the file names of
        the files that contain all words of the query as the keys
        and all Positions in that file of the words of the query as the values.  

        :param db: database containing file(s)
               query: input query
        """
        self.query = query
        t = Tokenizer()
        res = []  # list for dictionaries of search results
        fs = []  # list for sets of names of files
        output = {}
        dic = self.db
        for i in t.alph_tokenize(query):
            #print(i)
            if not dic.get(i.tok) in res:
                res.append(dic.get(i.tok))
        # create list of sets of filenames for each word
        for f in res:
            fs.append(set(f.keys()))
        for r in sorted(list(set.intersection(*fs)))[offset:offset+limit]:  # get files that contain all the words of the query
            for item in res:
                output.setdefault(r, []).append(item[r])
        # sort positions by line and start index
        for el in output:
            output[el] = our_sort(output[el])
        return output

    def search_stem(self, word, limit, offset):
        """One word search with stemming.

        :return: list of positions of the word stems/lemmas in the database
        :param word: input query word
               limit: number of files
               offset: index of the first file (starting at 1)
        """
        self.word = word
        res = {}
        output = {}
        dic = self.db
        stemmer = Stemmer_agent()
        for st in stemmer.stem(word):
            if st in dic:
                for fn in dic.get(st).keys():
                    res.setdefault(fn, []).extend(dic.get(st)[fn])
        keys = sorted(list(res.keys()))
        for num, k in enumerate(keys):
            if num >= offset and num < (offset + limit):
                output.setdefault(k, []).append(res[k])
        #print(output)
        for el in output:
            output[el] = our_sort(output[el])
        return output

    def search_mult_stem(self, query, limit, offset):
        """Multiword search with stemming.

        :return: a dictionary with the file names of
        the files that contain all stems/lemmas of the query words as the keys
        and a generator of all Positions query words stems/lemmas in that file.  

        :param query: input query
               limit: number of files
               offset: index of the first file (starting at 1)
        """
        t = Tokenizer()
        stemmer = Stemmer_agent()
        res = []  # list for dictionaries of search results
        fs = []  # list for sets of names of files
        output = {}
        dic = self.db
        for i in t.alph_tokenize(query):
            #print(i)
            stems = {}
            for st in stemmer.stem(i.tok):
                if st in dic:
                    #print(st)
                    for fn in dic.get(st).keys():
                        stems.setdefault(fn, []).extend(dic.get(st)[fn])
            res.append(stems)
        #for f in res:
         #   print(f)
        # create list of sets of filenames for each word
        for f in res:
            fs.append(set(f.keys()))
        for r in sorted(list(set.intersection(*fs)))[offset:offset+limit]:  # get files that contain all the words of the query
            for item in res:
                output.setdefault(r, []).append(item[r])
        # sort positions by line and start index
        for el in output:
            output[el] = our_sort(output[el])
        return output
