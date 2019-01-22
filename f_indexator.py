"""Module defining classes Position and Indexator"""

from tokenizer_gen import Token, Tokenizer
from morphan import Stemmer_agent
import shelve
import functools

class Position(object):
    """Class defining simple Position."""
    def __init__(self, start, end):
        """Construct Position object.

        :param start: start position
               end: end position
        """
        self.start = start
        self.end = end

    def __repr__(self):
        return "%s - %s" % (self.start, self.end)

    def __eq__(self, other):
        """Test two Position objects for equality"""
        return self.start == other.start and self.end == other.end

class Position_ext(Position):
    """Class defining more specific Position."""
    def __init__(self, start, end, path, line):
        """Construct Position_ext object.

        :param start: start position
               end: end position
               path: directory of the file
               line: line in the file
        """
        self.start = start
        self.end = end
        self.path = path
        self.line = line

    def __repr__(self):
        return "%s - %s; in %s, line %s. " % (self.start, self.end, self.path, self.line)

    def __eq__(self, other):
        """Test two Position_ext objects for equality"""
        return self.start == other.start and self.end == other.end and self.path == other.path and self.line == other.line


@functools.total_ordering
class Position_d(Position):
    """Class defining more specific position."""
    def __init__(self, start, end, line):
        """Construct Position_d object.

        :param start: start position
               end: end position
               line: line in the file
        """
        self.start = start
        self.end = end
        self.line = line

    def __repr__(self):
        return "%s - %s; line %s. " % (self.start, self.end, self.line)

    def __eq__(self, other):
        """Test two Position_d objects for equality"""
        return self.start == other.start and self.end == other.end and self.line == other.line

    def __lt__(self, other):
        return (self.line < other.line) or ((self.line == other.line) and (self.start < other.start))




class Indexator(object):
    """Class of Indexators.

    Methods:
    db_file_indexate -- return a database of Tokens and a dictionary of files and Position_d objects
    file_indexate -- return a dictionary of Tokens and Position_ext objects from a file
    indexate -- return a dictionary of Tokens and Position objects from a string
    lfile_indexate -- return a dictionary of Tokens and a dictionary of files and Position_d objects
    """

    def stem_indexate(self, name, s):
        """Indexate file and create a database.

        :return: database containing a dictionary of lemmas/stems
        and a dictionary of filenames where
        the lemma/stem were found and a list of Positions_d objects
        :param name: name of a file of a shelve database
               s: path of a indexated file
        """
        t = Tokenizer()
        stemmer = Stemmer_agent()
        db = shelve.open(name, 'c', writeback=True)
        with open(s, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                for it in t.i_tokenize(line):
                    if it.typ == "alph" or it.typ == "digit":
                        # get the stem or lemma of the token
                        for st in stemmer.stem(it.tok):
                            x = db.setdefault(st, {})
                            x.setdefault(s, []).append(Position_d(it.f_ch, it.l_ch, i))
        db.close()

    def db_file_indexate(self, name, s):
        """Indexate file and create a database.

        :return: database containing a dictionary of Tokens and a dictionary of filenames where
        the Token was found and a list of Positions_d objects
        :param name: name of a file of a shelve database
               s: path of a indexated file
        """
        self.name = name
        self.s = s
        t = Tokenizer()
        db = shelve.open(name, 'c', writeback=True)
        with open(s, 'r', encoding="utf-8") as f:
            for i, line in enumerate(f):
                for it in t.i_tokenize(line):
                    # include only alpha and digit tokens
                    if it.typ == "alph" or it.typ == "digit":
                        x = db.setdefault(it.tok, {})
                        x.setdefault(s, []).append(Position_d(it.f_ch, it.l_ch, i))
        db.close()

        
    def file_indexate(self, s):
        """Indexate a file.

        :return: dictionary of each unique Token from a file and a list of Position_ext
        :param s: path of the file
        """
        self.s = s
        d = {}
        t = Tokenizer()
        with open(s, 'r', encoding="utf-8") as f:
            for i, line in enumerate(f):
                for it in t.i_tokenize(line):
                    # include only alpha and digit tokens
                    if it.typ == "alph" or it.typ == "digit":
                        d.setdefault(it.tok, []).append(Position_ext(it.f_ch, it.l_ch, s, i))
        return d


    def indexate(self, s):
        """Indexate a string.

        :return: dictionary of each unique Token of a string and a list of its Positions
        :param s: indexated string
        """
        self.s = s
        d = {}
        t = Tokenizer()
        res = t.i_tokenize(s)
        for i in res:
            # include only alpha and digit tokens
            if i.typ == "alph" or i.typ == "digit":
                d.setdefault(i.tok, []).append(Position(i.f_ch, i.l_ch))
        return d

    
    def lfile_indexate(self, s):
        """Indexate a string from a file.

        :return: dictionary of each unique Token from a file and a list of Position_d for that Token
        :param s: path of the file
        """
        self.s = s
        d = {}
        t = Tokenizer()
        with open(s, 'r', encoding="utf-8") as f:
            for i, line in enumerate(f):
                for it in t.i_tokenize(line.lower()):
                    # include only alpha and digit tokens
                    if it.typ == "alph" or it.typ == "digit":
                        d.setdefault(it.tok, {}).setdefault(s, []).append(Position_d(it.f_ch, it.l_ch, i))
        return d
